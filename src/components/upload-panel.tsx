import { useState, useRef } from "react";
import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { Progress } from "./ui/progress";
import { Upload, File, CheckCircle2 } from "lucide-react";

interface UploadPanelProps {
  onUploadComplete: (fileName: string) => void;
}

export function UploadPanel({ onUploadComplete }: UploadPanelProps) {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadedFile, setUploadedFile] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setUploadProgress(0);
    setUploadedFile(file.name);

    // Симуляция загрузки
    const interval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsUploading(false);
          setTimeout(() => {
            onUploadComplete(file.name);
            setUploadedFile(null);
            setUploadProgress(0);
          }, 500);
          return 100;
        }
        return prev + 10;
      });
    }, 200);
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <Card className="p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-3 rounded-full bg-blue-100">
          <Upload className="w-6 h-6 text-blue-600" />
        </div>
        <div>
          <h3>Загрузка лекции</h3>
          <p className="text-gray-500">Поддерживаются форматы: MP3, MP4, WAV, M4A</p>
        </div>
      </div>

      {isUploading && uploadedFile && (
        <div className="mb-6 space-y-3">
          <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
            <File className="w-5 h-5 text-gray-400" />
            <span className="flex-1 truncate">{uploadedFile}</span>
          </div>
          
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Прогресс загрузки:</span>
              <span>{uploadProgress}%</span>
            </div>
            <Progress value={uploadProgress} />
          </div>
        </div>
      )}

      {uploadProgress === 100 && !isUploading && (
        <div className="mb-6 flex items-center gap-2 text-green-600 p-3 bg-green-50 rounded-lg">
          <CheckCircle2 className="w-5 h-5" />
          <span>Лекция успешно добавлена!</span>
        </div>
      )}

      <input
        ref={fileInputRef}
        type="file"
        accept="audio/*,video/*"
        onChange={handleFileSelect}
        className="hidden"
      />

      <Button 
        onClick={handleButtonClick}
        disabled={isUploading}
        className="w-full"
        variant="outline"
      >
        <Upload className="w-4 h-4 mr-2" />
        Выбрать файл
      </Button>
    </Card>
  );
}
