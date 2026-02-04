/**
 * Deepgram STT Provider
 *
 * Uses Deepgram's live streaming API for real-time transcription.
 * Compatible with the OpenClaw voice-call plugin interface.
 */

import WebSocket from "ws";

/**
 * Configuration for Deepgram STT.
 */
export interface DeepgramSTTConfig {
  /** Deepgram API key */
  apiKey: string;
  /** Model to use (default: nova-2) */
  model?: string;
  /** Language (default: en-US) */
  language?: string;
  /** Enable smart formatting */
  smartFormat?: boolean;
  /** Enable interim results */
  interimResults?: boolean;
  /** Endpointing silence threshold in ms (default: 800) */
  endpointingMs?: number;
}

/**
 * Session for streaming audio and receiving transcripts.
 */
export interface DeepgramSTTSession {
  connect(): Promise<void>;
  sendAudio(audio: Buffer): void;
  waitForTranscript(timeoutMs?: number): Promise<string>;
  onPartial(callback: (partial: string) => void): void;
  onTranscript(callback: (transcript: string) => void): void;
  onSpeechStart(callback: () => void): void;
  close(): void;
  isConnected(): boolean;
}

/**
 * Provider factory for Deepgram STT sessions.
 */
export class DeepgramSTTProvider {
  readonly name = "deepgram";
  private apiKey: string;
  private model: string;
  private language: string;
  private smartFormat: boolean;
  private interimResults: boolean;
  private endpointingMs: number;

  constructor(config: DeepgramSTTConfig) {
    if (!config.apiKey) {
      throw new Error("Deepgram API key required");
    }
    this.apiKey = config.apiKey;
    this.model = config.model || "nova-2";
    this.language = config.language || "en-US";
    this.smartFormat = config.smartFormat ?? true;
    this.interimResults = config.interimResults ?? true;
    this.endpointingMs = config.endpointingMs || 800;
  }

  createSession(): DeepgramSTTSession {
    return new DeepgramSTTSessionImpl(
      this.apiKey,
      this.model,
      this.language,
      this.smartFormat,
      this.interimResults,
      this.endpointingMs,
    );
  }
}

/**
 * WebSocket-based session for Deepgram real-time STT.
 */
class DeepgramSTTSessionImpl implements DeepgramSTTSession {
  private static readonly MAX_RECONNECT_ATTEMPTS = 5;
  private static readonly RECONNECT_DELAY_MS = 1000;

  private ws: WebSocket | null = null;
  private connected = false;
  private closed = false;
  private reconnectAttempts = 0;
  private pendingTranscript = "";
  private onTranscriptCallback: ((transcript: string) => void) | null = null;
  private onPartialCallback: ((partial: string) => void) | null = null;
  private onSpeechStartCallback: (() => void) | null = null;
  private speechStarted = false;

  constructor(
    private readonly apiKey: string,
    private readonly model: string,
    private readonly language: string,
    private readonly smartFormat: boolean,
    private readonly interimResults: boolean,
    private readonly endpointingMs: number,
  ) {}

  async connect(): Promise<void> {
    this.closed = false;
    this.reconnectAttempts = 0;
    return this.doConnect();
  }

  private async doConnect(): Promise<void> {
    return new Promise((resolve, reject) => {
      // Build Deepgram WebSocket URL with parameters
      const params = new URLSearchParams({
        model: this.model,
        language: this.language,
        encoding: "mulaw",
        sample_rate: "8000",
        channels: "1",
        smart_format: String(this.smartFormat),
        interim_results: String(this.interimResults),
        endpointing: String(this.endpointingMs),
        vad_events: "true",
      });

      const url = `wss://api.deepgram.com/v1/listen?${params.toString()}`;

      this.ws = new WebSocket(url, {
        headers: {
          Authorization: `Token ${this.apiKey}`,
        },
      });

      this.ws.on("open", () => {
        console.log("[DeepgramSTT] WebSocket connected");
        this.connected = true;
        this.reconnectAttempts = 0;
        resolve();
      });

      this.ws.on("message", (data: Buffer) => {
        try {
          const event = JSON.parse(data.toString());
          this.handleEvent(event);
        } catch (e) {
          console.error("[DeepgramSTT] Failed to parse event:", e);
        }
      });

      this.ws.on("error", (error) => {
        console.error("[DeepgramSTT] WebSocket error:", error);
        if (!this.connected) reject(error);
      });

      this.ws.on("close", (code, reason) => {
        console.log(
          `[DeepgramSTT] WebSocket closed (code: ${code}, reason: ${reason?.toString() || "none"})`,
        );
        this.connected = false;

        if (!this.closed) {
          void this.attemptReconnect();
        }
      });

      setTimeout(() => {
        if (!this.connected) {
          reject(new Error("Deepgram STT connection timeout"));
        }
      }, 10000);
    });
  }

  private async attemptReconnect(): Promise<void> {
    if (this.closed) return;

    if (this.reconnectAttempts >= DeepgramSTTSessionImpl.MAX_RECONNECT_ATTEMPTS) {
      console.error(
        `[DeepgramSTT] Max reconnect attempts (${DeepgramSTTSessionImpl.MAX_RECONNECT_ATTEMPTS}) reached`,
      );
      return;
    }

    this.reconnectAttempts++;
    const delay = DeepgramSTTSessionImpl.RECONNECT_DELAY_MS * 2 ** (this.reconnectAttempts - 1);
    console.log(
      `[DeepgramSTT] Reconnecting ${this.reconnectAttempts}/${DeepgramSTTSessionImpl.MAX_RECONNECT_ATTEMPTS} in ${delay}ms...`,
    );

    await new Promise((resolve) => setTimeout(resolve, delay));

    if (this.closed) return;

    try {
      await this.doConnect();
      console.log("[DeepgramSTT] Reconnected successfully");
    } catch (error) {
      console.error("[DeepgramSTT] Reconnect failed:", error);
    }
  }

  private handleEvent(event: {
    type?: string;
    is_final?: boolean;
    speech_final?: boolean;
    channel?: {
      alternatives?: Array<{ transcript?: string }>;
    };
  }): void {
    // Handle VAD speech start
    if (event.type === "SpeechStarted") {
      if (!this.speechStarted) {
        console.log("[DeepgramSTT] Speech started");
        this.speechStarted = true;
        this.pendingTranscript = "";
        this.onSpeechStartCallback?.();
      }
      return;
    }

    // Handle transcription results
    const transcript = event.channel?.alternatives?.[0]?.transcript || "";

    if (!transcript) return;

    if (event.is_final) {
      // Final result for this audio segment
      this.pendingTranscript += (this.pendingTranscript ? " " : "") + transcript;

      if (event.speech_final) {
        // End of speech detected - emit final transcript
        console.log(`[DeepgramSTT] Transcript: ${this.pendingTranscript}`);
        this.onTranscriptCallback?.(this.pendingTranscript.trim());
        this.pendingTranscript = "";
        this.speechStarted = false;
      } else {
        // Partial final - keep accumulating
        this.onPartialCallback?.(this.pendingTranscript);
      }
    } else {
      // Interim result
      const fullPartial = this.pendingTranscript + (this.pendingTranscript ? " " : "") + transcript;
      this.onPartialCallback?.(fullPartial);
    }
  }

  sendAudio(muLawData: Buffer): void {
    if (!this.connected || !this.ws || this.ws.readyState !== WebSocket.OPEN) return;
    // Deepgram accepts raw binary audio
    this.ws.send(muLawData);
  }

  onPartial(callback: (partial: string) => void): void {
    this.onPartialCallback = callback;
  }

  onTranscript(callback: (transcript: string) => void): void {
    this.onTranscriptCallback = callback;
  }

  onSpeechStart(callback: () => void): void {
    this.onSpeechStartCallback = callback;
  }

  async waitForTranscript(timeoutMs = 30000): Promise<string> {
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        this.onTranscriptCallback = null;
        reject(new Error("Transcript timeout"));
      }, timeoutMs);

      this.onTranscriptCallback = (transcript) => {
        clearTimeout(timeout);
        this.onTranscriptCallback = null;
        resolve(transcript);
      };
    });
  }

  close(): void {
    this.closed = true;
    if (this.ws) {
      // Send close frame to Deepgram
      if (this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: "CloseStream" }));
      }
      this.ws.close();
      this.ws = null;
    }
    this.connected = false;
  }

  isConnected(): boolean {
    return this.connected;
  }
}
