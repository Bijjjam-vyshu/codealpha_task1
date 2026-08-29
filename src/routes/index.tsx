import { createFileRoute } from "@tanstack/react-router";
import { useCallback, useEffect, useMemo, useState } from "react";
import { Eye, Heart, Lightbulb, RotateCcw, Trophy } from "lucide-react";
import { LEVELS, TOTAL_LEVELS } from "@/lib/words";
import { HangmanFigure } from "@/components/HangmanFigure";
import { LevelImage } from "@/components/LevelImage";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Hangman Quest — 500 Illustrated Levels" },
      {
        name: "description",
        content:
          "Play Hangman across 500 levels that get harder as you go, with an AI-drawn picture clue for every word and a difficulty menu for your lives.",
      },
      { property: "og:title", content: "Hangman Quest — 500 Illustrated Levels" },
      {
        property: "og:description",
        content:
          "500 levels of Hangman, easy to hard, with picture clues and adjustable difficulty.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Game,
});

const ALPHABET = "abcdefghijklmnopqrstuvwxyz".split("");
const PROGRESS_KEY = "hangman.progress.v1";

/** Difficulty presets: how many wrong guesses the round allows. */
const MAX_LIVES = 6; // never more than 6 wrong guesses
const DIFFICULTIES = [
  { name: "Classic", lives: 6, blurb: "The traditional hangman" },
  { name: "Steady", lives: 5, blurb: "One strike tighter" },
  { name: "Hard", lives: 4, blurb: "Every letter counts" },
  { name: "Brutal", lives: 3, blurb: "Three strikes, that's it" },
  { name: "Insane", lives: 2, blurb: "For sharp guessers only" },
];

type Phase = "menu" | "playing" | "won" | "lost";

function Game() {
  const [levelIndex, setLevelIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [phase, setPhase] = useState<Phase>("menu");
  const [maxWrong, setMaxWrong] = useState(6);
  const [guessed, setGuessed] = useState<string[]>([]);
  const [hintsUsed, setHintsUsed] = useState(0);
  const [showPicture, setShowPicture] = useState(false);
  const [shake, setShake] = useState(false);

  const level = LEVELS[Math.min(levelIndex, TOTAL_LEVELS - 1)]!;
  const secret = level.word;

  // Restore progress from the last session.
  useEffect(() => {
    const raw = localStorage.getItem(PROGRESS_KEY);
    if (!raw) return;
    try {
      const saved = JSON.parse(raw) as { levelIndex?: number; score?: number; maxWrong?: number };
      if (typeof saved.levelIndex === "number")
        setLevelIndex(Math.min(Math.max(saved.levelIndex, 0), TOTAL_LEVELS - 1));
      if (typeof saved.score === "number") setScore(saved.score);
      if (typeof saved.maxWrong === "number") setMaxWrong(saved.maxWrong);
    } catch {
      /* ignore corrupt progress */
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(PROGRESS_KEY, JSON.stringify({ levelIndex, score, maxWrong }));
  }, [levelIndex, score, maxWrong]);

  const wrong = useMemo(
    () => guessed.filter((letter) => !secret.includes(letter)).length,
    [guessed, secret],
  );
  const livesLeft = maxWrong - wrong;
  const solved = useMemo(
    () => secret.split("").every((letter) => guessed.includes(letter)),
    [guessed, secret],
  );

  const startRound = useCallback((lives: number) => {
    setMaxWrong(lives);
    setGuessed([]);
    setHintsUsed(0);
    setShowPicture(false);
    setPhase("playing");
  }, []);

  const guess = useCallback(
    (letter: string) => {
      if (phase !== "playing" || guessed.includes(letter)) return;
      const next = [...guessed, letter];
      setGuessed(next);

      if (!secret.includes(letter)) {
        setShake(true);
        setTimeout(() => setShake(false), 400);
        const wrongNow = next.filter((l) => !secret.includes(l)).length;
        if (wrongNow >= maxWrong) setPhase("lost");
        return;
      }

      if (secret.split("").every((l) => next.includes(l))) {
        // +10 base, plus a bonus for playing on tighter difficulty.
        setScore((s) => s + 10 + Math.max(0, 10 - maxWrong) * 2);
        setPhase("won");
      }
    },
    [guessed, maxWrong, phase, secret],
  );

  // Physical keyboard support.
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      const key = event.key.toLowerCase();
      if (key.length === 1 && key >= "a" && key <= "z") guess(key);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [guess]);

  // Longer words get more hints: roughly one hint per three letters (min 2).
  const maxHints = Math.max(2, Math.floor(new Set(secret.split("")).size / 3));
  const hintsLeft = maxHints - hintsUsed;

  const useHint = () => {
    if (hintsLeft <= 0 || phase !== "playing") return;
    const remaining = Array.from(new Set(secret.split(""))).filter((l) => !guessed.includes(l));
    if (remaining.length <= 1) return; // keep the final letter for the player
    setHintsUsed((n) => n + 1);
    guess(remaining[Math.floor(Math.random() * remaining.length)]!);
  };

  const nextLevel = () => {
    setLevelIndex((i) => Math.min(i + 1, TOTAL_LEVELS - 1));
    setPhase("menu");
  };

  const resetProgress = () => {
    setLevelIndex(0);
    setScore(0);
    setPhase("menu");
  };

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-5xl flex-col gap-6 px-4 py-8 sm:px-6">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl leading-tight text-primary sm:text-4xl">Hangman Quest</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            500 levels, easy to hard — with a picture clue for every word.
          </p>
        </div>
        <div className="flex items-center gap-4 text-sm">
          <div className="chalk-panel px-4 py-2 text-center">
            <div className="text-xs uppercase tracking-wide text-muted-foreground">Level</div>
            <div className="font-display text-lg text-chalk">
              {level.level}
              <span className="text-sm text-muted-foreground">/{TOTAL_LEVELS}</span>
            </div>
          </div>
          <div className="chalk-panel px-4 py-2 text-center">
            <div className="text-xs uppercase tracking-wide text-muted-foreground">Score</div>
            <div className="font-display text-lg text-primary">{score}</div>
          </div>
        </div>
      </header>

      {phase === "menu" ? (
        <section className="chalk-panel flex flex-col gap-5 p-6 sm:p-8">
          <div>
            <h2 className="text-xl text-chalk">Choose your difficulty</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              Level {level.level} · {level.category} · {secret.length} letters. Pick how many wrong
              guesses you can afford.
            </p>
          </div>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {DIFFICULTIES.map((option) => (
              <button
                key={option.name}
                onClick={() => startRound(option.lives)}
                className="group rounded-xl border border-border bg-secondary p-4 text-left transition-all hover:-translate-y-0.5 hover:border-primary hover:bg-muted focus-visible:outline-2 focus-visible:outline-ring"
              >
                <div className="flex items-center justify-between">
                  <span className="font-display text-base text-chalk">{option.name}</span>
                  <span className="flex items-center gap-1 text-sm text-primary">
                    <Heart className="h-4 w-4 fill-current" />
                    {option.lives}
                  </span>
                </div>
                <p className="mt-1 text-xs text-muted-foreground">{option.blurb}</p>
              </button>
            ))}
          </div>
          <div className="flex flex-wrap items-center gap-3 border-t border-border pt-4">
            <label className="text-sm text-muted-foreground" htmlFor="custom-lives">
              Or set your own:
            </label>
            <input
              id="custom-lives"
              type="number"
              min={1}
              max={MAX_LIVES}
              defaultValue={6}
              className="w-20 rounded-md border border-border bg-input px-3 py-1.5 text-sm text-chalk"
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  const value = Number((e.target as HTMLInputElement).value);
                  if (value >= 1 && value <= MAX_LIVES) startRound(value);
                }
              }}
            />
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                const input = document.getElementById("custom-lives") as HTMLInputElement | null;
                const value = Number(input?.value ?? 6);
                startRound(Math.min(MAX_LIVES, Math.max(1, value || 6)));
              }}
            >
              Start round
            </Button>
            <Button variant="ghost" size="sm" className="ml-auto" onClick={resetProgress}>
              <RotateCcw className="mr-1 h-4 w-4" /> Reset progress
            </Button>
          </div>
        </section>
      ) : (
        <section className="grid gap-6 lg:grid-cols-[1fr_320px]">
          <div className="chalk-panel flex flex-col gap-6 p-6">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <span className="rounded-full bg-secondary px-3 py-1 text-xs uppercase tracking-wide text-accent">
                {level.category}
              </span>
              <div className="flex items-center gap-1.5">
                {Array.from({ length: maxWrong }).map((_, i) => (
                  <Heart
                    key={i}
                    className={`h-4 w-4 ${
                      i < livesLeft ? "fill-current text-destructive" : "text-muted"
                    }`}
                  />
                ))}
                <span className="ml-2 text-sm text-muted-foreground">
                  {livesLeft} left of {maxWrong}
                </span>
              </div>
            </div>

            <div className={`mx-auto h-48 w-48 ${shake ? "animate-shake" : ""}`}>
              <HangmanFigure wrong={wrong} maxWrong={maxWrong} />
            </div>

            <div className="flex flex-wrap justify-center gap-2 sm:gap-3">
              {secret.split("").map((letter, i) => {
                const revealedLetter = guessed.includes(letter) || phase !== "playing";
                return (
                  <span
                    key={`${letter}-${i}`}
                    className="flex h-12 w-9 items-end justify-center border-b-4 border-border pb-1 sm:h-14 sm:w-11"
                  >
                    {revealedLetter && (
                      <span
                        className={`slot-letter animate-pop-in text-2xl uppercase sm:text-3xl ${
                          phase === "lost" && !guessed.includes(letter) ? "text-destructive" : ""
                        }`}
                      >
                        {letter}
                      </span>
                    )}
                  </span>
                );
              })}
            </div>

            {phase === "playing" ? (
              <>
                <div className="grid grid-cols-7 gap-1.5 sm:grid-cols-9 sm:gap-2">
                  {ALPHABET.map((letter) => {
                    const used = guessed.includes(letter);
                    const hit = used && secret.includes(letter);
                    return (
                      <button
                        key={letter}
                        onClick={() => guess(letter)}
                        disabled={used}
                        className={`rounded-md py-2 font-display text-sm uppercase transition-all ${
                          hit
                            ? "bg-success text-success-foreground"
                            : used
                              ? "bg-muted text-muted-foreground line-through"
                              : "bg-secondary text-chalk hover:-translate-y-0.5 hover:bg-primary hover:text-primary-foreground"
                        }`}
                      >
                        {letter}
                      </button>
                    );
                  })}
                </div>
                <div className="flex flex-wrap gap-2">
                  <Button variant="outline" size="sm" onClick={useHint} disabled={hintsLeft <= 0}>
                    <Lightbulb className="mr-1 h-4 w-4" />
                    {hintsLeft > 0 ? `Reveal a letter (${hintsLeft} left)` : "No hints left"}
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setShowPicture(true)}
                    disabled={showPicture}
                  >
                    <Eye className="mr-1 h-4 w-4" />
                    {showPicture ? "Picture shown" : "Show picture clue"}
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="ml-auto"
                    onClick={() => setPhase("menu")}
                  >
                    Change difficulty
                  </Button>
                </div>
              </>
            ) : (
              <div className="flex flex-col items-center gap-3 rounded-xl border border-border bg-secondary p-5 text-center">
                <h2
                  className={`text-2xl ${phase === "won" ? "text-success" : "text-destructive"}`}
                >
                  {phase === "won" ? "You Win!" : "Game Over!"}
                </h2>
                <p className="text-sm text-muted-foreground">
                  The word was <span className="uppercase text-chalk">{secret}</span>.{" "}
                  {phase === "won"
                    ? `+${10 + Math.max(0, 10 - maxWrong) * 2} points`
                    : "No points this time."}
                </p>
                <div className="flex flex-wrap justify-center gap-2">
                  {phase === "won" ? (
                    <Button onClick={nextLevel}>
                      <Trophy className="mr-1 h-4 w-4" /> Next level
                    </Button>
                  ) : (
                    <Button onClick={() => setPhase("menu")}>
                      <RotateCcw className="mr-1 h-4 w-4" /> Try level again
                    </Button>
                  )}
                  <Button variant="outline" onClick={nextLevel}>
                    Skip to level {Math.min(level.level + 1, TOTAL_LEVELS)}
                  </Button>
                </div>
              </div>
            )}
          </div>

          <aside className="chalk-panel flex flex-col gap-3 p-5">
            <h2 className="text-base text-chalk">Picture clue</h2>
            <LevelImage
              word={secret}
              category={level.category}
              revealed={showPicture || phase !== "playing"}
            />
            <p className="text-xs text-muted-foreground">
              {showPicture || phase !== "playing"
                ? "Drawn just for this word."
                : "Stuck? Reveal the illustration for this level's word."}
            </p>
          </aside>
        </section>
      )}
    </main>
  );
}
