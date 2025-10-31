import { useEffect, useMemo, useState } from "react";
import { BookOpen } from "lucide-react";

import { RecordingPanel } from "./components/recording-panel";
import { UploadPanel } from "./components/upload-panel";
import { LectureLibrary } from "./components/lecture-library";
import { LectureView } from "./components/lecture-view";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { Toaster } from "./components/ui/sonner";
import { toast } from "sonner";
import { deleteNote, getNoteDetail, listNotes } from "./lib/api";
import type { NoteDetail, NoteListItem } from "./types";

function toListItem(note: NoteDetail): NoteListItem {
  const { content, ...rest } = note;
  return rest;
}

export default function App() {
  const [notes, setNotes] = useState<NoteListItem[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [selectedNote, setSelectedNote] = useState<NoteDetail | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [loadingList, setLoadingList] = useState(false);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      setLoadingList(true);
      setError(null);
      try {
        const items = await listNotes();
        setNotes(items);
      } catch (err) {
        console.error(err);
        setError(err instanceof Error ? err.message : "Failed to load notes");
      } finally {
        setLoadingList(false);
      }
    };
    load();
  }, []);

  const handleSelectLecture = async (id: number) => {
    setLoadingDetail(true);
    setError(null);
    try {
      const detail = await getNoteDetail(id);
      setSelectedNote(detail);
      setSelectedId(id);
    } catch (err) {
      console.error(err);
      setError(err instanceof Error ? err.message : "Failed to load note");
    } finally {
      setLoadingDetail(false);
    }
  };

  const handleDeleteLecture = async (id: number) => {
    try {
      await deleteNote(id);
      setNotes((prev) => prev.filter((note) => note.id !== id));
      if (selectedId === id) {
        setSelectedId(null);
        setSelectedNote(null);
      }
      toast.success("Note deleted");
    } catch (err) {
      console.error(err);
      toast.error("Failed to delete note");
    }
  };

  const handleNoteCreated = (note: NoteDetail) => {
    const listItem = toListItem(note);
    setNotes((prev) => {
      const filtered = prev.filter((n) => n.id !== note.id);
      return [listItem, ...filtered];
    });
    setSelectedId(note.id);
    setSelectedNote(note);
    toast.success("Note ready", {
      description: note.summary ?? "Transcription and summary completed",
    });
  };

  const visibleNotes = useMemo(() => {
    if (!searchQuery.trim()) {
      return notes;
    }
    const lower = searchQuery.trim().toLowerCase();
    return notes.filter((note) => note.title.toLowerCase().includes(lower));
  }, [notes, searchQuery]);

  const renderContent = () => {
    if (selectedNote && selectedId !== null) {
      return (
        <div className="min-h-screen bg-gray-50">
          <div className="container mx-auto px-4 py-8 max-w-5xl">
            <LectureView
              note={selectedNote}
              isLoading={loadingDetail}
              onBack={() => {
                setSelectedId(null);
                setSelectedNote(null);
              }}
            />
          </div>
          <Toaster />
        </div>
      );
    }

    return (
      <div className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8 max-w-7xl">
          <div className="mb-8">
            <div className="flex items-center gap-3 mb-2">
              <div className="p-3 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl">
                <BookOpen className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                  LectureSynth
                </h1>
                <p className="text-gray-600">Record, transcribe, summarise.</p>
              </div>
            </div>
            {error && <p className="text-sm text-red-600">{error}</p>}
          </div>

          <div className="grid lg:grid-cols-3 gap-6">
            <div className="lg:col-span-1 space-y-6">
              <Tabs defaultValue="record" className="w-full">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="record">Record</TabsTrigger>
                  <TabsTrigger value="upload">Upload</TabsTrigger>
                </TabsList>

                <TabsContent value="record" className="mt-6">
                  <RecordingPanel onNoteCreated={handleNoteCreated} />
                </TabsContent>

                <TabsContent value="upload" className="mt-6">
                  <UploadPanel onNoteCreated={handleNoteCreated} />
                </TabsContent>
              </Tabs>
            </div>

            <div className="lg:col-span-2">
              <div className="mb-4">
                <h2 className="text-xl font-semibold">Library</h2>
                <p className="text-gray-500">
                  Notes captured: {notes.length}
                </p>
              </div>

              <LectureLibrary
                isLoading={loadingList}
                notes={visibleNotes}
                selectedId={selectedId}
                onSelect={handleSelectLecture}
                onDelete={handleDeleteLecture}
                searchQuery={searchQuery}
                onSearchChange={setSearchQuery}
              />
            </div>
          </div>
        </div>

        <Toaster />
      </div>
    );
  };

  return renderContent();
}
