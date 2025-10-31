import { useState } from "react";
import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { Progress } from "./ui/progress";
import { ArrowLeft, FileDown, Sparkles } from "lucide-react";

interface TranscriptSegment {
  timestamp: string;
  text: string;
  keywords?: string[];
}

interface LectureViewProps {
  lecture: {
    id: string;
    title: string;
    date: string;
    hasTranscript: boolean;
  };
  onBack: () => void;
}

export function LectureView({ lecture, onBack }: LectureViewProps) {
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationProgress, setGenerationProgress] = useState(0);
  const [transcript, setTranscript] = useState<TranscriptSegment[] | null>(
    lecture.hasTranscript ? [
      {
        timestamp: "00:00",
        text: "Добро пожаловать на сегодняшнюю лекцию по машинному обучению. Сегодня мы будем обсуждать нейронные сети и их применение в современных системах искусственного интеллекта.",
        keywords: ["машинное обучение", "нейронные сети", "искусственный интеллект"]
      },
      {
        timestamp: "00:45",
        text: "Начнем с основ. Нейронная сеть - это вычислительная модель, вдохновленная биологическими нейронными сетями в человеческом мозге. Она состоит из слоев взаимосвязанных узлов, которые мы называем нейронами.",
        keywords: ["нейронная сеть", "нейроны"]
      },
      {
        timestamp: "01:30",
        text: "Ключевыми компонентами нейронной сети являются входной слой, скрытые слои и выходной слой. Данные проходят через эти слои, преобразуясь на каждом этапе с помощью весовых коэффициентов и функций активации.",
        keywords: ["входной слой", "скрытые слои", "выходной слой", "весовые коэффициенты"]
      },
      {
        timestamp: "02:15",
        text: "Процесс обучения нейронной сети основан на алгоритме обратного распространения ошибки. Мы подаем данные, получаем предсказание, вычисляем ошибку и корректируем веса для минимизации этой ошибки.",
        keywords: ["обратное распространение", "обучение", "предсказание"]
      },
      {
        timestamp: "03:00",
        text: "Давайте рассмотрим практические применения. Нейронные сети используются в распознавании изображений, обработке естественного языка, автономных транспортных средствах и многих других областях.",
        keywords: ["распознавание изображений", "обработка языка", "применения"]
      }
    ] : null
  );

  const handleGenerateTranscript = () => {
    setIsGenerating(true);
    setGenerationProgress(0);

    const interval = setInterval(() => {
      setGenerationProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsGenerating(false);
          setTranscript([
            {
              timestamp: "00:00",
              text: "Добро пожаловать на сегодняшнюю лекцию по машинному обучению. Сегодня мы будем обсуждать нейронные сети и их применение в современных системах искусственного интеллекта.",
              keywords: ["машинное обучение", "нейронные сети", "искусственный интеллект"]
            },
            {
              timestamp: "00:45",
              text: "Начнем с основ. Нейронная сеть - это вычислительная модель, вдохновленная биологическими нейронными сетями в человеческом мозге. Она состоит из слоев взаимосвязанных узлов, которые мы называем нейронами.",
              keywords: ["нейронная сеть", "нейроны"]
            }
          ]);
          return 100;
        }
        return prev + 10;
      });
    }, 300);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Button variant="ghost" onClick={onBack}>
          <ArrowLeft className="w-4 h-4 mr-2" />
          Назад к библиотеке
        </Button>
        
        {transcript && (
          <Button variant="outline">
            <FileDown className="w-4 h-4 mr-2" />
            Экспортировать
          </Button>
        )}
      </div>

      <Card className="p-6">
        <div className="mb-6">
          <h2 className="mb-2">{lecture.title}</h2>
          <p className="text-gray-500">{lecture.date}</p>
        </div>

        {!transcript && !isGenerating && (
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Sparkles className="w-8 h-8 text-purple-600" />
            </div>
            <h3 className="mb-2">Конспект не сформирован</h3>
            <p className="text-gray-500 mb-6">
              Нажмите кнопку ниже, чтобы автоматически создать конспект лекции
            </p>
            <Button onClick={handleGenerateTranscript}>
              <Sparkles className="w-4 h-4 mr-2" />
              Сформировать конспект
            </Button>
          </div>
        )}

        {isGenerating && (
          <div className="py-12 space-y-4">
            <div className="text-center mb-6">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
                <Sparkles className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="mb-2">Формирование конспекта</h3>
              <p className="text-gray-500">Пожалуйста, подождите...</p>
            </div>
            
            <div className="max-w-md mx-auto space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Прогресс:</span>
                <span>{generationProgress}%</span>
              </div>
              <Progress value={generationProgress} />
            </div>
          </div>
        )}

        {transcript && !isGenerating && (
          <div className="space-y-6">
            <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg border border-green-200">
              <span className="text-green-800">Конспект готов</span>
              <Badge variant="secondary" className="bg-green-600">
                {transcript.length} сегментов
              </Badge>
            </div>

            <div className="space-y-4">
              {transcript.map((segment, idx) => (
                <div key={idx} className="p-4 border rounded-lg hover:bg-gray-50 transition-colors">
                  <div className="flex items-start gap-4">
                    <div className="flex-shrink-0 mt-1">
                      <Badge variant="outline" className="tabular-nums">
                        {segment.timestamp}
                      </Badge>
                    </div>
                    
                    <div className="flex-1">
                      <p className="mb-3">{segment.text}</p>
                      
                      {segment.keywords && segment.keywords.length > 0 && (
                        <div className="flex gap-2 flex-wrap">
                          {segment.keywords.map((keyword, kidx) => (
                            <Badge key={kidx} className="bg-purple-100 text-purple-800 hover:bg-purple-200">
                              {keyword}
                            </Badge>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}
