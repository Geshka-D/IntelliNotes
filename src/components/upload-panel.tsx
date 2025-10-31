import { useRef, useState } from "react";
import { Upload, File, Loader2 } from "lucide-react";
import { toast } from "sonner";

import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Progress } from "./ui/progress";
import type { NoteDetail } from "../types";
import { createNoteFromUpload } from "../lib/api";

interface UploadPanelProps {
  onNoteCreated: (note: NoteDetail) => void;
}

export function UploadPanel({ onNoteCreated }: UploadPanelProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [fileName, setFileName] = useState<string | null>(null);

  const reset = () => {
    setIsUploading(false);
    setProgress(0);
    setFileName(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setProgress(10);
    setFileName(file.name);

    let progressInterval: ReturnType<typeof setInterval> | undefined;
    try {
      // Simulate progress while upload completes.
      progressInterval = setInterval(() => {
        setProgress((prev) => Math.min(prev + 10, 90));
      }, 150);

      const note = await createNoteFromUpload(file, file.name.replace(/\.[^/.]+$/, ""));
      if (progressInterval) {
        clearInterval(progressInterval);
      }
      setProgress(100);
      onNoteCreated(note);
      toast.success("Upload processed", {
        description: note.summary ?? "Transcription completed successfully",
      });
    } catch (err) {
      console.error(err);
      toast.error(err instanceof Error ? err.message : "Failed to process file");
    } finally {
      if (progressInterval) {
        clearInterval(progressInterval);
      }
      setTimeout(reset, 600);
    }
  };

  return (
    <Card className="p-6 space-y-6">
      <div className="flex items-center gap-3">
        <div className="p-3 rounded-full bg-blue-100">
          <Upload className="w-6 h-6 text-blue-600" />
        </div>
        <div>
          <h3 className="font-semibold">Upload recording</h3>
          <p className="text-sm text-gray-500">Supported formats: MP3, MP4, WAV, M4A.</p>
        </div>
      </div>

      {isUploading && fileName && (
        <div className="space-y-3">
          <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
            <File className="w-5 h-5 text-gray-400" />
            <span className="flex-1 truncate text-sm">{fileName}</span>
            <span className="text-sm text-gray-500">{progress}%</span>
          </div>
          <Progress value={progress} />
        </div>
      )}

      <input
        ref={fileInputRef}
        type="file"
        accept="audio/*,video/*"
        onChange={handleFileSelect}
        className="hidden"
      />

      <Button onClick={() => fileInputRef.current?.click()} disabled={isUploading} variant="outline" className="w-full">
        {isUploading ? (
          <>
            <Loader2 className="w-4 h-4 mr-2 animate-spin" /> Processing�
          </>
        ) : (
          <>
            <Upload className="w-4 h-4 mr-2" /> Choose a file
          </>
        )}
      </Button>
    </Card>
  );
}
