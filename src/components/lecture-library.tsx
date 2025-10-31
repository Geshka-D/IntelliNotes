import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Input } from "./ui/input";
import { Calendar, FileText, Loader2, Trash2 } from "lucide-react";
import type { NoteListItem } from "../types";

interface LectureLibraryProps {
  notes: NoteListItem[];
  selectedId: number | null;
  onSelect: (id: number) => void;
  onDelete: (id: number) => void;
  searchQuery: string;
  onSearchChange: (query: string) => void;
  isLoading: boolean;
}

const STATUS_LABELS: Record<string, string> = {
  ready: "Ready",
  recorded: "Recorded",
  processing: "Processing",
};

const STATUS_CLASSES: Record<string, string> = {
  ready: "bg-green-500",
  recorded: "bg-blue-500",
  processing: "bg-yellow-500",
};

export function LectureLibrary({
  notes,
  selectedId,
  onSelect,
  onDelete,
  searchQuery,
  onSearchChange,
  isLoading,
}: LectureLibraryProps) {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="relative flex-1">
          <Input
            type="text"
            placeholder="Search notes..."
            value={searchQuery}
            onChange={(event) => onSearchChange(event.target.value)}
            className="pl-3"
          />
        </div>
      </div>

      {isLoading ? (
        <Card className="p-8 text-center">
          <Loader2 className="w-10 h-10 mx-auto mb-4 animate-spin text-gray-400" />
          <p className="text-gray-500">Loading notes…</p>
        </Card>
      ) : notes.length === 0 ? (
        <Card className="p-8 text-center">
          <FileText className="w-12 h-12 mx-auto mb-4 text-gray-300" />
          <p className="text-gray-500">No notes captured yet.</p>
          <p className="text-gray-400 mt-1">
            Start a recording or upload a file to create one.
          </p>
        </Card>
      ) : (
        <div className="grid gap-4">
          {notes.map((note) => {
            const statusLabel = STATUS_LABELS[note.status] ?? note.status;
            const statusClass = STATUS_CLASSES[note.status] ?? "bg-gray-500";

            return (
              <Card
                key={note.id}
                className={`p-4 transition-shadow hover:shadow-md ${
                  selectedId === note.id ? "border-blue-500 shadow-md" : ""
                }`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0 space-y-2">
                    <div className="flex items-center gap-2">
                      <h3 className="truncate font-semibold">{note.title}</h3>
                      <Badge className={statusClass}>{statusLabel}</Badge>
                    </div>
                    <div className="flex items-center gap-4 text-sm text-gray-500">
                      <div className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        <span>
                          {note.created_at
                            ? new Date(note.created_at).toLocaleString()
                            : "—"}
                        </span>
                      </div>
                      <span>{note.language?.toUpperCase() ?? "AUTO"}</span>
                    </div>
                    {note.summary && (
                      <p className="text-gray-600 line-clamp-2">{note.summary}</p>
                    )}
                    {note.keywords.length > 0 && (
                      <div className="flex flex-wrap gap-2">
                        {note.keywords.slice(0, 4).map((keyword) => (
                          <Badge key={keyword} variant="outline">
                            {keyword}
                          </Badge>
                        ))}
                      </div>
                    )}
                  </div>

                  <div className="flex flex-col gap-2">
                    <Button
                      variant="default"
                      size="sm"
                      onClick={() => onSelect(note.id)}
                    >
                      View
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => onDelete(note.id)}
                    >
                      <Trash2 className="w-4 h-4 text-red-500" />
                    </Button>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
