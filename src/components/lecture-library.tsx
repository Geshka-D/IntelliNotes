import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { Input } from "./ui/input";
import { Search, Calendar, FileText, Trash2, Eye } from "lucide-react";

export interface Lecture {
  id: string;
  title: string;
  date: string;
  duration?: string;
  status: 'processing' | 'ready' | 'recorded';
  tags?: string[];
  hasTranscript: boolean;
}

interface LectureLibraryProps {
  lectures: Lecture[];
  onSelectLecture: (id: string) => void;
  onDeleteLecture: (id: string) => void;
  searchQuery: string;
  onSearchChange: (query: string) => void;
}

export function LectureLibrary({ 
  lectures, 
  onSelectLecture, 
  onDeleteLecture,
  searchQuery,
  onSearchChange 
}: LectureLibraryProps) {
  const getStatusColor = (status: Lecture['status']) => {
    switch(status) {
      case 'processing': return 'bg-yellow-500';
      case 'ready': return 'bg-green-500';
      case 'recorded': return 'bg-blue-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusText = (status: Lecture['status']) => {
    switch(status) {
      case 'processing': return 'Обработка';
      case 'ready': return 'Готово';
      case 'recorded': return 'Записано';
      default: return '';
    }
  };

  const filteredLectures = lectures.filter(lecture => 
    lecture.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <Input
            type="text"
            placeholder="Поиск лекций..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      <div className="grid gap-4">
        {filteredLectures.length === 0 ? (
          <Card className="p-8 text-center">
            <FileText className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p className="text-gray-500">Лекции не найдены</p>
            <p className="text-gray-400 mt-1">Начните запись или загрузите файл</p>
          </Card>
        ) : (
          filteredLectures.map((lecture) => (
            <Card key={lecture.id} className="p-4 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="truncate">{lecture.title}</h3>
                    <Badge variant="secondary" className={getStatusColor(status)}>
                      {getStatusText(lecture.status)}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center gap-4 text-gray-500 mb-2">
                    <div className="flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      <span>{lecture.date}</span>
                    </div>
                    {lecture.duration && (
                      <span>{lecture.duration}</span>
                    )}
                  </div>

                  {lecture.tags && lecture.tags.length > 0 && (
                    <div className="flex gap-2 flex-wrap">
                      {lecture.tags.map((tag, idx) => (
                        <Badge key={idx} variant="outline">
                          {tag}
                        </Badge>
                      ))}
                    </div>
                  )}
                </div>

                <div className="flex gap-2">
                  {lecture.hasTranscript && (
                    <Button
                      variant="default"
                      size="sm"
                      onClick={() => onSelectLecture(lecture.id)}
                    >
                      <Eye className="w-4 h-4 mr-2" />
                      Открыть
                    </Button>
                  )}
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => onDeleteLecture(lecture.id)}
                  >
                    <Trash2 className="w-4 h-4 text-red-500" />
                  </Button>
                </div>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
