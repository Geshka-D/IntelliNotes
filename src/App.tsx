import { useState } from "react";
import { RecordingPanel } from "./components/recording-panel";
import { UploadPanel } from "./components/upload-panel";
import { LectureLibrary, Lecture } from "./components/lecture-library";
import { LectureView } from "./components/lecture-view";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { BookOpen } from "lucide-react";
import { Toaster } from "./components/ui/sonner";
import { toast } from "sonner@2.0.3";

export default function App() {
  const [selectedLectureId, setSelectedLectureId] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [lectures, setLectures] = useState<Lecture[]>([
    {
      id: "1",
      title: "Введение в машинное обучение",
      date: "20.10.2025",
      duration: "45:23",
      status: "ready",
      tags: ["ML", "AI", "Основы"],
      hasTranscript: true
    },
    {
      id: "2",
      title: "Алгоритмы сортировки",
      date: "18.10.2025",
      duration: "32:15",
      status: "ready",
      tags: ["Алгоритмы", "CS"],
      hasTranscript: true
    },
    {
      id: "3",
      title: "Веб-разработка с React",
      date: "15.10.2025",
      duration: "58:40",
      status: "processing",
      tags: ["React", "Frontend"],
      hasTranscript: false
    }
  ]);

  const handleRecordingComplete = (title: string, duration: string) => {
    const newLecture: Lecture = {
      id: Date.now().toString(),
      title,
      date: new Date().toLocaleDateString('ru-RU'),
      duration,
      status: "recorded",
      hasTranscript: false
    };
    
    setLectures(prev => [newLecture, ...prev]);
    toast.success("Запись завершена", {
      description: `Лекция "${title}" успешно сохранена`
    });
  };

  const handleUploadComplete = (fileName: string) => {
    const newLecture: Lecture = {
      id: Date.now().toString(),
      title: fileName.replace(/\.[^/.]+$/, ""),
      date: new Date().toLocaleDateString('ru-RU'),
      status: "processing",
      hasTranscript: false
    };
    
    setLectures(prev => [newLecture, ...prev]);
    toast.success("Файл загружен", {
      description: "Начата обработка лекции"
    });
  };

  const handleDeleteLecture = (id: string) => {
    setLectures(prev => prev.filter(l => l.id !== id));
    toast.success("Лекция удалена");
  };

  const selectedLecture = selectedLectureId 
    ? lectures.find(l => l.id === selectedLectureId)
    : null;

  if (selectedLecture) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8 max-w-5xl">
          <LectureView 
            lecture={selectedLecture} 
            onBack={() => setSelectedLectureId(null)} 
          />
        </div>
        <Toaster />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-3 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl">
              <BookOpen className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                LectureSynth
              </h1>
              <p className="text-gray-600">Автоматическое конспектирование лекций</p>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Left Column - Actions */}
          <div className="lg:col-span-1 space-y-6">
            <Tabs defaultValue="record" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="record">Запись</TabsTrigger>
                <TabsTrigger value="upload">Загрузка</TabsTrigger>
              </TabsList>
              
              <TabsContent value="record" className="mt-6">
                <RecordingPanel onRecordingComplete={handleRecordingComplete} />
              </TabsContent>
              
              <TabsContent value="upload" className="mt-6">
                <UploadPanel onUploadComplete={handleUploadComplete} />
              </TabsContent>
            </Tabs>
          </div>

          {/* Right Column - Library */}
          <div className="lg:col-span-2">
            <div className="mb-4">
              <h2>Библиотека лекций</h2>
              <p className="text-gray-500">Всего лекций: {lectures.length}</p>
            </div>
            
            <LectureLibrary
              lectures={lectures}
              onSelectLecture={setSelectedLectureId}
              onDeleteLecture={handleDeleteLecture}
              searchQuery={searchQuery}
              onSearchChange={setSearchQuery}
            />
          </div>
        </div>
      </div>
      
      <Toaster />
    </div>
  );
}
