import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { ArrowLeft, CheckCircle2, ListChecks, Sparkles } from "lucide-react";
import type { NoteDetail } from "../types";

interface LectureViewProps {
  note: NoteDetail;
  onBack: () => void;
  isLoading: boolean;
}

export function LectureView({ note, onBack, isLoading }: LectureViewProps) {
  const {
    summary,
    bullets,
    decisions,
    action_items,
    open_questions,
    keywords,
    links,
    content,
    created_at,
    language,
    summarizer_provider,
  } = note;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Button variant="ghost" onClick={onBack} className="flex items-center gap-2">
          <ArrowLeft className="w-4 h-4" />
          Back to list
        </Button>
        <div className="text-sm text-gray-500">
          <span>{created_at ? new Date(created_at).toLocaleString() : ""}</span>
          {language && <span className="ml-2 uppercase">{language}</span>}
        </div>
      </div>

      <Card className="p-6 space-y-4">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-blue-600/10 rounded-full">
            <Sparkles className="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <h2 className="text-xl font-semibold">Summary</h2>
            <p className="text-sm text-gray-500">
              Provider: {summarizer_provider ?? "extractive"}
            </p>
          </div>
        </div>
        {isLoading ? (
          <p className="text-gray-500">Loading note…</p>
        ) : summary ? (
          <p className="text-gray-700 leading-relaxed">{summary}</p>
        ) : (
          <p className="text-gray-400">Summary unavailable.</p>
        )}
      </Card>

      {bullets.length > 0 && (
        <Card className="p-6 space-y-3">
          <h3 className="font-semibold">Key points</h3>
          <ul className="list-disc ml-5 space-y-2 text-gray-700">
            {bullets.map((point, idx) => (
              <li key={idx}>{point}</li>
            ))}
          </ul>
        </Card>
      )}

      {keywords.length > 0 && (
        <Card className="p-6 space-y-3">
          <h3 className="font-semibold">Keywords</h3>
          <div className="flex flex-wrap gap-2">
            {keywords.map((keyword) => (
              <Badge key={keyword} variant="outline">
                {keyword}
              </Badge>
            ))}
          </div>
        </Card>
      )}

      <div className="grid md:grid-cols-2 gap-4">
        {decisions.length > 0 && (
          <Card className="p-6 space-y-3">
            <h3 className="font-semibold flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-green-600" /> Decisions
            </h3>
            <ul className="list-disc ml-5 space-y-2 text-gray-700">
              {decisions.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </Card>
        )}

        {action_items.length > 0 && (
          <Card className="p-6 space-y-3">
            <h3 className="font-semibold flex items-center gap-2">
              <ListChecks className="w-4 h-4 text-blue-600" /> Action items
            </h3>
            <ul className="list-disc ml-5 space-y-2 text-gray-700">
              {action_items.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </Card>
        )}
      </div>

      {open_questions.length > 0 && (
        <Card className="p-6 space-y-3">
          <h3 className="font-semibold">Open questions</h3>
          <ul className="list-disc ml-5 space-y-2 text-gray-700">
            {open_questions.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </Card>
      )}

      {links.length > 0 && (
        <Card className="p-6 space-y-3">
          <h3 className="font-semibold">Suggested reading</h3>
          <ul className="space-y-2 text-sm">
            {links.map((link, idx) => (
              <li key={idx}>
                <a
                  href={link.url ?? "#"}
                  target="_blank"
                  rel="noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  {link.title ?? link.term ?? link.url}
                </a>
                {link.summary && <p className="text-gray-500">{link.summary}</p>}
              </li>
            ))}
          </ul>
        </Card>
      )}

      <Card className="p-6 space-y-3">
        <h3 className="font-semibold">Transcript</h3>
        {content ? (
          <div className="prose max-w-none whitespace-pre-wrap text-gray-800">
            {content}
          </div>
        ) : (
          <p className="text-gray-400">Transcript is not available for this note.</p>
        )}
      </Card>
    </div>
  );
}
