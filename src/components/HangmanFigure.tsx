interface HangmanFigureProps {
  /** Wrong guesses so far. */
  wrong: number;
  /** Wrong guesses allowed this round (set by the difficulty menu). */
  maxWrong: number;
}

/**
 * Gallows drawing. There are always 6 body parts, so the drawing is scaled to
 * whatever number of allowed mistakes the player picked in the difficulty menu.
 */
export function HangmanFigure({ wrong, maxWrong }: HangmanFigureProps) {
  const parts = Math.min(6, Math.round((wrong / maxWrong) * 6));
  const show = (n: number) => (parts >= n ? "opacity-100" : "opacity-0");

  return (
    <svg viewBox="0 0 200 220" className="h-full w-full" role="img" aria-label="Hangman drawing">
      <g
        stroke="var(--color-chalk)"
        strokeWidth="5"
        strokeLinecap="round"
        fill="none"
        opacity="0.55"
      >
        <line x1="20" y1="205" x2="120" y2="205" />
        <line x1="55" y1="205" x2="55" y2="20" />
        <line x1="55" y1="20" x2="135" y2="20" />
        <line x1="135" y1="20" x2="135" y2="45" />
      </g>
      <g
        stroke="var(--color-primary)"
        strokeWidth="5"
        strokeLinecap="round"
        fill="none"
        className="transition-opacity duration-300"
      >
        <circle cx="135" cy="63" r="18" className={`transition-opacity duration-300 ${show(1)}`} />
        <line
          x1="135"
          y1="81"
          x2="135"
          y2="140"
          className={`transition-opacity duration-300 ${show(2)}`}
        />
        <line
          x1="135"
          y1="95"
          x2="110"
          y2="120"
          className={`transition-opacity duration-300 ${show(3)}`}
        />
        <line
          x1="135"
          y1="95"
          x2="160"
          y2="120"
          className={`transition-opacity duration-300 ${show(4)}`}
        />
        <line
          x1="135"
          y1="140"
          x2="112"
          y2="180"
          className={`transition-opacity duration-300 ${show(5)}`}
        />
        <line
          x1="135"
          y1="140"
          x2="158"
          y2="180"
          className={`transition-opacity duration-300 ${show(6)}`}
        />
      </g>
    </svg>
  );
}
