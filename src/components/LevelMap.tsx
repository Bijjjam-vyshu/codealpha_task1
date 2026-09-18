import { Check, Lock, Star } from "lucide-react";
import { LEVELS, TOTAL_LEVELS } from "@/lib/words";

type Props = {
  /** Zero-based index of the level the player is on. */
  currentIndex: number;
  /** Jump back to an already-cleared level. */
  onSelect: (index: number) => void;
};

/** How many stops of the route to show around the player. */
const BEFORE = 3;
const AFTER = 8;

/**
 * A winding "route map" of levels: cleared stops behind you, your current stop,
 * and the road ahead. Stops alternate up and down along a dashed path.
 */
export function LevelMap({ currentIndex, onSelect }: Props) {
  const start = Math.max(0, currentIndex - BEFORE);
  const end = Math.min(TOTAL_LEVELS, currentIndex + AFTER + 1);
  const stops = LEVELS.slice(start, end).map((level, i) => ({ level, index: start + i }));

  return (
    <div className="relative overflow-x-auto pb-2">
      {/* the road */}
      <div className="pointer-events-none absolute inset-x-0 top-1/2 h-1 -translate-y-1/2 rounded-full bg-[repeating-linear-gradient(90deg,var(--color-border)_0_14px,transparent_14px_26px)]" />

      <ol className="relative flex min-w-max items-center gap-4 px-2 py-8">
        {stops.map(({ level, index }) => {
          const cleared = index < currentIndex;
          const current = index === currentIndex;
          const locked = index > currentIndex;
          const lifted = index % 2 === 0;

          return (
            <li
              key={level.level}
              className={lifted ? "-translate-y-6" : "translate-y-6"}
            >
              <button
                type="button"
                disabled={!cleared && !current}
                onClick={() => onSelect(index)}
                title={`Level ${level.level} · ${level.category}`}
                className={`flex h-16 w-16 flex-col items-center justify-center rounded-full border-2 transition-all ${
                  current
                    ? "scale-110 border-primary bg-primary text-primary-foreground shadow-[0_0_28px_var(--color-primary)]"
                    : cleared
                      ? "border-accent bg-secondary text-accent hover:-translate-y-0.5"
                      : "border-border bg-muted text-muted-foreground opacity-70"
                }`}
              >
                {current ? (
                  <Star className="h-4 w-4 fill-current" />
                ) : cleared ? (
                  <Check className="h-4 w-4" />
                ) : (
                  <Lock className="h-3.5 w-3.5" />
                )}
                <span className="font-display text-sm leading-none mt-1">{level.level}</span>
              </button>
              <div className="mt-1 w-16 truncate text-center text-[10px] uppercase tracking-wide text-muted-foreground">
                {locked ? "???" : level.category}
              </div>
            </li>
          );
        })}
      </ol>
    </div>
  );
}
