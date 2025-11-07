import { useCallback, useEffect, useState } from "react";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Progress } from "./ui/progress";
import { Loader2, Mic, Square } from "lucide-react";
import { toast } from "sonner";
import { createNoteFromRecording, startRecording, stopRecording } from "../lib/api";
import type { NoteDetail } from "../types";

interface RecordingPanelProps {
  onNoteCreated: (note: NoteDetail) => void;
}

export function RecordingPanel({ onNoteCreated }: RecordingPanelProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioLevel, setAudioLevel] = useState(0);
  const [deviceName, setDeviceName] = useState<string | null>(null);

  useEffect(() => {
    let interval: ReturnType<typeof setInterval> | undefined;
    if (isRecording) {
      interval = setInterval(() => {
        setRecordingTime((prev) => prev + 1);
        setAudioLevel(Math.round(Math.random() * 100));
      }, 1000);
    } else {
      setRecordingTime(0);
      setAudioLevel(0);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isRecording]);

  const formatTime = useCallback((seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs
      .toString()
      .padStart(2, "0")}`;
  }, []);

  const handleStartRecording = async () => {
    try {
      const response = await startRecording();
      setIsRecording(true);
      setDeviceName(response.device_name ?? null);
      toast.success("Recording started");
    } catch (err) {
      console.error(err);
      const message = err instanceof Error ? err.message : "Failed to start recording";
      toast.error(message);
    }
  };

  const handleStopRecording = async () => {
    setIsRecording(false);
    setIsProcessing(true);
    try {
      const response = await stopRecording();
      if (!response.filename) {
        toast.error("Recording did not produce a file");
        return;
      }
      const title = `Recording ${new Date().toLocaleString()}`;
      const note = await createNoteFromRecording(response.filename, title);
      onNoteCreated(note);
    } catch (err) {
      console.error(err);
      const message = err instanceof Error ? err.message : "Failed to process recording";
      toast.error(message);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <Card className="p-6 space-y-6">
      <div className="flex items-center gap-3">
        <div className={`p-3 rounded-full ${isRecording ? "bg-red-100" : "bg-gray-100"}`}>
          <Mic className={`w-6 h-6 ${isRecording ? "text-red-600" : "text-gray-600"}`} />
        </div>
        <div>
          <h3 className="font-semibold">Record lecture</h3>
          <p className="text-sm text-gray-500">
            {isRecording ? "Capturing system audio…" : "Start recording loopback audio."}
          </p>
          {deviceName && <p className="text-sm text-gray-400">Device: {deviceName}</p>}
        </div>
      </div>

      {(isRecording || isProcessing) && (
        <div className="space-y-4">
          <div className="flex items-center justify-between text-sm text-gray-600">
            <span>Elapsed time:</span>
            <span className="tabular-nums">{formatTime(recordingTime)}</span>
          </div>
          {isRecording && (
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm text-gray-600">
                <span>Signal level:</span>
                <span>{audioLevel}%</span>
              </div>
              <Progress value={audioLevel} className="h-2" />
            </div>
          )}
        </div>
      )}

      <div className="flex gap-3">
        {!isRecording ? (
          <Button onClick={handleStartRecording} className="flex-1" disabled={isProcessing}>
            <Mic className="w-4 h-4 mr-2" /> Start recording
          </Button>
        ) : (
          <Button
            onClick={handleStopRecording}
            variant="destructive"
            className="flex-1"
            disabled={isProcessing}
          >
            <Square className="w-4 h-4 mr-2" /> Stop recording
          </Button>
        )}
      </div>

      {isProcessing && (
        <div className="flex items-center gap-2 text-sm text-gray-500">
          <Loader2 className="w-4 h-4 animate-spin" />
          Processing transcription…
        </div>
      )}
    </Card>
  );
}
