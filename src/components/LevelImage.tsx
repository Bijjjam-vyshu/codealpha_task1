import { useEffect, useState } from "react";
import { ImageIcon, Loader2 } from "lucide-react";
import { streamImage } from "@/lib/streamImage";

// In-memory cache so replaying a level doesn't regenerate its picture.
const cache = new Map<string, string>();

interface LevelImageProps {
  word: string;
  category: string;
  /** Hide the picture until the player asks for it. */
  revealed: boolean;
}

export function LevelImage({ word, category, revealed }: LevelImageProps) {
  const [src, setSrc] = useState<string | null>(cache.get(word) ?? null);
  const [isFinal, setIsFinal] = useState(cache.has(word));
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setSrc(cache.get(word) ?? null);
    setIsFinal(cache.has(word));
    setError(null);
    if (!revealed || cache.has(word)) return;

    let cancelled = false;
    const prompt = `A friendly, colorful flat vector illustration of a ${word} (${category}). Simple bold shapes, soft shadows, centered subject, plain warm background, no text, no letters, no words.`;

    streamImage("/api/generate-image", prompt, (dataUrl, final) => {
      if (cancelled) return;
      setSrc(dataUrl);
      if (final) {
        setIsFinal(true);
        cache.set(word, dataUrl);
      }
    }).catch((err: Error) => {
      if (!cancelled) setError(err.message);
    });

    return () => {
      cancelled = true;
    };
  }, [word, category, revealed]);

  return (
    <div className="relative aspect-square w-full overflow-hidden rounded-xl bg-muted">
      {src ? (
        <img
          src={src}
          alt={revealed ? `Illustration for the level word` : ""}
          className={`h-full w-full object-cover transition-[filter] duration-500 ${
            isFinal ? "blur-0" : "blur-2xl"
          }`}
        />
      ) : (
        <div className="flex h-full w-full flex-col items-center justify-center gap-2 px-4 text-center text-sm text-muted-foreground">
          {error ? (
            <span className="text-destructive">{error}</span>
          ) : revealed ? (
            <>
              <Loader2 className="h-6 w-6 animate-spin" />
              Drawing your picture clue…
            </>
          ) : (
            <>
              <ImageIcon className="h-6 w-6" />
              Picture clue hidden
            </>
          )}
        </div>
      )}
    </div>
  );
}
