import { useState, useEffect } from "react";
import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { Progress } from "./ui/progress";
import { Mic, Square, Circle } from "lucide-react";

interface RecordingPanelProps {
  onRecordingComplete: (title: string, duration: string) => void;
}

export function RecordingPanel({ onRecordingComplete }: RecordingPanelProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioLevel, setAudioLevel] = useState(0);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (isRecording) {
      interval = setInterval(() => {
        setRecordingTime(prev => prev + 1);
        // Симуляция уровня звука
        setAudioLevel(Math.random() * 100);
      }, 1000);
    } else {
      setRecordingTime(0);
      setAudioLevel(0);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isRecording]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleStartRecording = () => {
    setIsRecording(true);
  };

  const handleStopRecording = () => {
    setIsRecording(false);
    const duration = formatTime(recordingTime);
    const title = `Лекция от ${new Date().toLocaleDateString('ru-RU')}`;
    onRecordingComplete(title, duration);
  };

  return (
    <Card className="p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className={`p-3 rounded-full ${isRecording ? 'bg-red-100' : 'bg-gray-100'}`}>
          <Mic className={`w-6 h-6 ${isRecording ? 'text-red-600' : 'text-gray-600'}`} />
        </div>
        <div>
          <h3>Запись лекции</h3>
          <p className="text-gray-500">
            {isRecording ? 'Идет запись системного звука' : 'Нажмите кнопку для начала записи'}
          </p>
        </div>
      </div>

      {isRecording && (
        <div className="space-y-4 mb-6">
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Время записи:</span>
            <span className="tabular-nums">{formatTime(recordingTime)}</span>
          </div>
          
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Уровень звука:</span>
              <span>{Math.round(audioLevel)}%</span>
            </div>
            <Progress value={audioLevel} className="h-2" />
          </div>
        </div>
      )}

      <div className="flex gap-3">
        {!isRecording ? (
          <Button 
            onClick={handleStartRecording}
            className="flex-1"
          >
            <Circle className="w-4 h-4 mr-2 fill-current" />
            Начать запись
          </Button>
        ) : (
          <Button 
            onClick={handleStopRecording}
            variant="destructive"
            className="flex-1"
          >
            <Square className="w-4 h-4 mr-2" />
            Остановить запись
          </Button>
        )}
      </div>

      {isRecording && (
        <div className="mt-4 flex items-center gap-2 text-red-600 animate-pulse">
          <div className="w-3 h-3 bg-red-600 rounded-full"></div>
          <span>Запись в процессе</span>
        </div>
      )}
    </Card>
  );
}
