# AI Agent Replication Guide: Modern Landing Page Style & Structure

This document provides comprehensive instructions for AI agents to replicate the design system, structure, and styling patterns used in this Next.js landing page application.

## Table of Contents

1. [Tech Stack & Dependencies](#tech-stack--dependencies)
2. [Project Structure](#project-structure)
3. [Design System](#design-system)
4. [Styling Approach](#styling-approach)
5. [Component Patterns](#component-patterns)
6. [Typography & Spacing](#typography--spacing)
7. [Color System](#color-system)
8. [Layout & Responsive Design](#layout--responsive-design)
9. [Animations & Interactions](#animations--interactions)
10. [Accessibility & UX](#accessibility--ux)
11. [Implementation Checklist](#implementation-checklist)

---

## Tech Stack & Dependencies

### Core Framework

- **Next.js 14+** (App Router)
- **React 18+**
- **TypeScript 5+**

### UI Libraries & Tools

- **shadcn/ui** - Component library built on Radix UI
- **Tailwind CSS 3.4+** - Utility-first CSS framework
- **Radix UI Primitives** - Accessible UI primitives
  - `@radix-ui/react-accordion`
  - `@radix-ui/react-dialog`
  - `@radix-ui/react-slot`
  - `@radix-ui/react-toast`
- **Lucide React** - Icon library
- **canvas-confetti** - Animation library for celebratory effects

### Utility Libraries

- **class-variance-authority** - Component variant management
- **clsx** - Conditional class names
- **tailwind-merge** - Merge Tailwind classes intelligently

### Font

- **Inter** (Google Fonts) - Primary typeface, loaded via `next/font/google`

---

## Project Structure

```
project-root/
├── app/
│   ├── globals.css          # Global styles, CSS variables, Tailwind directives
│   ├── layout.tsx           # Root layout with metadata and font setup
│   ├── page.tsx             # Main landing page composition
│   ├── privacy/
│   │   └── page.tsx         # Privacy policy page
│   └── terms/
│       └── page.tsx         # Terms of service page
├── components/
│   ├── landing/             # Feature-specific landing components
│   │   ├── Header.tsx       # Sticky navigation header
│   │   ├── Hero.tsx         # Hero section with CTA
│   │   ├── Features.tsx     # Feature grid cards
│   │   ├── Pricing.tsx      # Pricing cards with interactions
│   │   ├── FAQ.tsx          # Accordion-based FAQ
│   │   ├── Footer.tsx       # Footer with links
│   │   ├── ContactDialog.tsx # Modal dialog for contact
│   │   ├── CopyableEmail.tsx # Email copy component
│   │   └── ScrollToTop.tsx  # Scroll-to-top button
│   ├── ui/                  # Reusable shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── accordion.tsx
│   │   ├── dialog.tsx
│   │   ├── toast.tsx
│   │   └── toaster.tsx
│   └── ScrollRestoration.tsx # Scroll position management
├── hooks/
│   └── use-toast.ts         # Toast notification hook
├── lib/
│   └── utils.ts             # Utility functions (cn helper)
├── components.json           # shadcn/ui configuration
├── tailwind.config.ts       # Tailwind configuration with theme
├── tsconfig.json            # TypeScript configuration
└── package.json             # Dependencies

```

### Key Structural Principles

1. **Feature-based component organization**: Landing-specific components live in `components/landing/`
2. **Reusable UI primitives**: shadcn/ui components in `components/ui/`
3. **Utility separation**: Helper functions in `lib/` and hooks in `hooks/`
4. **Path aliases**: Use `@/` prefix for imports (configured in `tsconfig.json`)

---

## Design System

### Core Design Principles

1. **Clean & Minimal**: Uncluttered layouts with generous white space
2. **Consistent Spacing**: Use Tailwind's spacing scale systematically
3. **Semantic HTML**: Proper heading hierarchy (h1 → h2 → h3)
4. **Accessible**: WCAG compliant with proper ARIA labels
5. **Mobile-First**: Responsive design starting from mobile breakpoints

### Visual Hierarchy

- **Hero Section**: Largest text (4xl-7xl), bold, high contrast
- **Section Headings**: 3xl-5xl, bold, centered
- **Card Titles**: xl-2xl, semibold
- **Body Text**: base-lg, regular weight, muted colors for descriptions

---

## Styling Approach

### CSS Variables (HSL Format)

All colors are defined as CSS variables in HSL format for easy theming:

```css
:root {
  --background: 0 0% 100%;           /* White */
  --foreground: 222.2 84% 4.9%;      /* Near black */
  --primary: 222.2 47.4% 11.2%;      /* Dark blue-gray */
  --primary-foreground: 210 40% 98%; /* Near white */
  --muted: 210 40% 96.1%;           /* Light gray */
  --muted-foreground: 215.4 16.3% 46.9%; /* Medium gray */
  --border: 214.3 31.8% 91.4%;      /* Light border */
  --radius: 0.5rem;                 /* Border radius */
}
```

**Usage in Tailwind**: `bg-primary`, `text-foreground`, `border-border`

### Dark Mode Support

The design system includes dark mode variables. To activate, add `class="dark"` to the root element or use `darkMode: ["class"]` in Tailwind config.

### Utility Function: `cn()`

Always use the `cn()` utility from `@/lib/utils` to merge class names:

```typescript
import { cn } from "@/lib/utils"

// Combines clsx and tailwind-merge for intelligent class merging
className={cn("base-class", conditionalClass && "active-class", props.className)}
```

---

## Component Patterns

### 1. Section Components

All main sections follow this pattern:

```typescript
export function SectionName() {
  return (
    <section id="section-id" className="container mx-auto px-4 py-16 md:py-24">
      <div className="text-center mb-16">
        <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
          Section Title
        </h2>
        <p className="text-muted-foreground text-base md:text-lg max-w-2xl mx-auto">
          Section description
        </p>
      </div>
      {/* Section content */}
    </section>
  )
}
```

**Key patterns:**

- Container with centered max-width
- Responsive padding: `py-16 md:py-24`
- Centered header section with consistent typography
- Max-width constraints on description text (`max-w-2xl mx-auto`)

### 2. Card Components

Use shadcn/ui Card components:

```typescript
<Card className="h-full transition-shadow hover:shadow-lg">
  <CardHeader>
    <CardTitle className="text-xl">Title</CardTitle>
  </CardHeader>
  <CardContent>
    <CardDescription className="text-base leading-relaxed">
      Description
    </CardDescription>
  </CardContent>
</Card>
```

**Styling notes:**

- Always use `h-full` on cards in grids for equal height
- Add `transition-shadow hover:shadow-lg` for hover effects
- Use `leading-relaxed` for readable body text

### 3. Button Components

Button variants follow shadcn/ui patterns:

```typescript
<Button asChild size="lg" className="text-base px-8">
  <Link href="#section">Action</Link>
</Button>
```

**Variants:**

- `default`: Primary action (solid background)
- `outline`: Secondary action (border only)
- `ghost`: Minimal style for icons/navigation
- `destructive`: Delete/danger actions

**Sizes:**

- `sm`: Compact
- `default`: Standard
- `lg`: Prominent CTAs

### 4. Navigation Header

Sticky header with backdrop blur:

```typescript
<header className="border-b sticky top-0 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 z-50">
  <div className="container mx-auto px-4 py-4 flex items-center justify-between">
    {/* Logo and nav */}
  </div>
</header>
```

**Key features:**

- Sticky positioning with high z-index
- Backdrop blur with fallback
- Semi-transparent background
- Mobile-responsive navigation menu

---

## Typography & Spacing

### Typography Scale

```typescript
// Hero Title
className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-6 leading-tight"

// Section Headings
className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4"

// Card Titles
className="text-xl" // or "text-2xl" for larger cards

// Body Text
className="text-base md:text-lg" // Standard
className="text-sm" // Smaller text (descriptions, footers)

// Muted Text
className="text-muted-foreground"
```

### Spacing Scale

**Vertical Spacing:**

- Between sections: `py-16 md:py-24`
- Section header to content: `mb-16`
- Card internal spacing: `p-6` (CardHeader, CardContent)
- Element gaps: `gap-4`, `gap-6` for grids
- Small gaps: `gap-2`, `space-y-2`

**Horizontal Spacing:**

- Container padding: `px-4`
- Button padding: `px-4` (default), `px-8` (lg)
- Max content width: `max-w-4xl` (hero), `max-w-2xl` (descriptions), `max-w-3xl` (FAQ)

### Line Height

- Headings: `leading-tight` (tight)
- Body text: `leading-relaxed` (comfortable reading)
- Default: Inherit from Tailwind defaults

---

## Color System

### Color Usage Guidelines

1. **Background**: `bg-background` - Main page background
2. **Foreground**: `text-foreground` - Primary text color
3. **Primary**: `bg-primary text-primary-foreground` - Main brand color for CTAs
4. **Muted**: `text-muted-foreground` - Secondary text, descriptions
5. **Border**: `border-border` - Consistent border color
6. **Card**: `bg-card text-card-foreground` - Card backgrounds

### Highlight Pattern

For highlighted elements (e.g., featured pricing plan):

```typescript
className={cn(
  "base-classes",
  isHighlighted && "border-primary shadow-md ring-2 ring-primary/20"
)}
```

---

## Layout & Responsive Design

### Container Pattern

Always use the container pattern:

```typescript
<div className="container mx-auto px-4">
  {/* Content */}
</div>
```

This provides:

- Centered content with max-width
- Responsive horizontal padding
- Consistent margins

### Grid Layouts

**Feature Cards (3 columns):**

```typescript
<div className="grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
```

**Pricing Cards (4 columns):**

```typescript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
```

**Footer (3 columns):**

```typescript
<div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
```

### Responsive Breakpoints (Tailwind Default)

- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1400px (container max-width)

### Mobile-First Approach

1. Design for mobile first
2. Use `md:` prefix for tablet/desktop styles
3. Stack vertically on mobile, horizontal on larger screens
4. Hide/show elements with `hidden md:flex` or `md:hidden`

---

## Animations & Interactions

### Scroll Animations

Custom CSS utility classes in `globals.css`:

```css
.scroll-section {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}

.scroll-section.visible {
  opacity: 1;
  transform: translateY(0);
}
```

### Hover Effects

**Cards:**

```typescript
className="transition-shadow hover:shadow-lg"
```

**Links:**

```typescript
className="hover:text-primary transition-colors"
```

**Buttons:** Built into shadcn/ui button component

### Smooth Scrolling

Configured globally in `globals.css`:

```css
html {
  scroll-behavior: smooth;
  scroll-padding-top: 80px; /* Account for sticky header */
}
```

### Celebratory Animations

Use `canvas-confetti` for positive user actions:

```typescript
import confetti from "canvas-confetti"

// Trigger confetti on button click or success action
const triggerConfetti = () => {
  // Configure and fire confetti
}
```

---

## Accessibility & UX

### Semantic HTML

- Use proper heading hierarchy (h1 → h2 → h3)
- Use `<nav>`, `<header>`, `<footer>`, `<section>` elements
- Use `<button>` for actions, `<a>` for navigation

### ARIA Labels

```typescript
<Button
  aria-label="Toggle menu"
  onClick={handleClick}
>
  {/* Icon */}
</Button>
```

### Focus States

Built into shadcn/ui components with:

- Visible focus rings
- Keyboard navigation support
- `focus-visible` styles

### Mobile Menu

- Hamburger icon for mobile
- Slide-out or dropdown menu
- Close on link click
- Accessible keyboard navigation

### Scroll Restoration

Implement `ScrollRestoration` component to:

- Save scroll position on scroll
- Restore position on page load/restore
- Handle browser tab restoration
- Prevent scroll jumps

---

## Implementation Checklist

### Setup Phase

- [ ] Install Next.js 14+ with TypeScript
- [ ] Install and configure Tailwind CSS
- [ ] Install shadcn/ui and configure `components.json`
- [ ] Set up path aliases (`@/*`) in `tsconfig.json`
- [ ] Install required dependencies (Radix UI, Lucide, etc.)
- [ ] Configure Inter font via `next/font/google`

### Configuration Files

- [ ] `tailwind.config.ts`: Configure theme with CSS variables
- [ ] `globals.css`: Add CSS variables, Tailwind directives, custom utilities
- [ ] `components.json`: Configure shadcn/ui paths and settings
- [ ] `tsconfig.json`: Configure path aliases and compiler options

### Core Components

- [ ] Create `lib/utils.ts` with `cn()` function
- [ ] Install shadcn/ui components: button, card, accordion, dialog, toast
- [ ] Create `ScrollRestoration` component
- [ ] Set up toast system (`hooks/use-toast.ts`, `components/ui/toaster.tsx`)

### Landing Components

- [ ] `Header`: Sticky nav with mobile menu
- [ ] `Hero`: Large heading, description, CTA buttons
- [ ] `Features`: Grid of feature cards
- [ ] `Pricing`: Pricing cards with highlight support
- [ ] `FAQ`: Accordion-based FAQ section
- [ ] `Footer`: Multi-column footer with links
- [ ] `ContactDialog`: Modal with copy functionality
- [ ] `ScrollToTop`: Back-to-top button (if needed)

### Styling

- [ ] Apply consistent spacing patterns
- [ ] Use CSS variables for all colors
- [ ] Implement responsive typography scale
- [ ] Add hover and transition effects
- [ ] Configure smooth scrolling
- [ ] Test dark mode (if implementing)

### Layout Structure

- [ ] Create `app/layout.tsx` with font and metadata
- [ ] Create `app/page.tsx` composing all landing sections
- [ ] Ensure proper semantic HTML structure
- [ ] Add section IDs for anchor navigation

### Polish & Testing

- [ ] Test responsive design on all breakpoints
- [ ] Verify accessibility (keyboard navigation, ARIA labels)
- [ ] Test smooth scrolling behavior
- [ ] Verify scroll restoration works
- [ ] Test interactive elements (buttons, dialogs, accordions)
- [ ] Ensure proper color contrast ratios
- [ ] Test on mobile devices

---

## Code Examples

### Example: Hero Section

```typescript
import { Button } from "@/components/ui/button"
import Link from "next/link"

export function Hero() {
  return (
    <section className="container mx-auto px-4 py-16 md:py-24">
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-6 leading-tight">
          Main Headline
          <br />
          <span className="text-primary">Highlighted Text</span>
        </h1>
        <p className="text-lg md:text-xl lg:text-2xl text-muted-foreground mb-8 max-w-2xl mx-auto leading-relaxed">
          Description text that explains the value proposition.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button asChild size="lg" className="text-base px-8">
            <Link href="#get-started">Get Started</Link>
          </Button>
          <Button asChild variant="outline" size="lg" className="text-base px-8">
            <Link href="#features">Learn More</Link>
          </Button>
        </div>
      </div>
    </section>
  )
}
```

### Example: Feature Grid

```typescript
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

const features = [
  { title: "Feature 1", description: "Description..." },
  { title: "Feature 2", description: "Description..." },
]

export function Features() {
  return (
    <section id="features" className="container mx-auto px-4 py-16 md:py-24">
      <div className="text-center mb-16">
        <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
          Features
        </h2>
        <p className="text-muted-foreground text-base md:text-lg max-w-2xl mx-auto">
          Description of features section
        </p>
      </div>
      <div className="grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {features.map((feature, index) => (
          <Card key={index} className="h-full transition-shadow hover:shadow-lg">
            <CardHeader>
              <CardTitle className="text-xl">{feature.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-base leading-relaxed">
                {feature.description}
              </CardDescription>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  )
}
```

---

## Best Practices

1. **Consistency**: Use the same patterns across all components
2. **Reusability**: Extract common patterns into reusable components
3. **Accessibility**: Always include proper ARIA labels and semantic HTML
4. **Performance**: Use `"use client"` only when necessary (for interactivity)
5. **Type Safety**: Use TypeScript for all components and props
6. **Code Organization**: Keep feature components separate from UI primitives
7. **Responsive Design**: Test on multiple screen sizes
8. **Loading States**: Consider loading states for dynamic content
9. **Error Handling**: Handle edge cases gracefully
10. **Documentation**: Comment complex logic or business rules

---

## Additional Notes

- The design uses a **minimal, professional aesthetic** with subtle animations
- **White space** is used generously for visual breathing room
- **Card-based layouts** create clear content separation
- **Consistent typography scale** ensures visual hierarchy
- **Smooth interactions** (transitions, hover effects) enhance UX
- **Mobile-first responsive design** ensures accessibility on all devices

---

**Last Updated**: Based on the current codebase structure and styling patterns.
