import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const articleSchema = z.object({
  title: z.string(),
  description: z.string(),
  slug: z.string(),
  keyword: z.string(),
  author: z.string(),
  date: z.string(),
  image: z.string().optional(),
});

const blogSchema = articleSchema.extend({
  lastUpdated: z.string().optional(),
  category: z.enum(['SEO Tools', 'Content Strategy', 'Local SEO', 'SEO Tips']),
});

const glossarySchema = z.object({
  term: z.string(),
  slug: z.string(),
  definition: z.string(),
  category: z.enum(['Marketing', 'SEO', 'Local SEO', 'Social Media', 'AI & Emerging']),
  difficulty: z.enum(['Beginner', 'Intermediate', 'Advanced']),
  relatedTerms: z.array(z.string()).optional(),
  keyword: z.string(),
  date: z.string(),
  lastUpdated: z.string().optional(),
});

// English collections
const reviews = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/reviews' }),
  schema: articleSchema,
});

const alternatives = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/alternatives' }),
  schema: articleSchema,
});

const best = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/best' }),
  schema: articleSchema,
});

const glossary = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/glossary' }),
  schema: glossarySchema,
});

const compare = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/compare' }),
  schema: articleSchema,
});

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: blogSchema,
});

// German (de)
const blog_de = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog_de' }),
  schema: blogSchema,
});
const glossary_de = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/glossary_de' }),
  schema: glossarySchema,
});
const reviews_de = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/reviews_de' }),
  schema: articleSchema,
});
const alternatives_de = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/alternatives_de' }),
  schema: articleSchema,
});
const best_de = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/best_de' }),
  schema: articleSchema,
});
const compare_de = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/compare_de' }),
  schema: articleSchema,
});

// French (fr)
const compare_fr = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/compare_fr' }),
  schema: articleSchema,
});
const blog_fr = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog_fr' }),
  schema: blogSchema,
});
const glossary_fr = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/glossary_fr' }),
  schema: glossarySchema,
});
const reviews_fr = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/reviews_fr' }),
  schema: articleSchema,
});
const alternatives_fr = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/alternatives_fr' }),
  schema: articleSchema,
});
const best_fr = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/best_fr' }),
  schema: articleSchema,
});

// Spanish (es)
const blog_es = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog_es' }),
  schema: blogSchema,
});
const glossary_es = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/glossary_es' }),
  schema: glossarySchema,
});
const reviews_es = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/reviews_es' }),
  schema: articleSchema,
});
const alternatives_es = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/alternatives_es' }),
  schema: articleSchema,
});
const best_es = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/best_es' }),
  schema: articleSchema,
});
const compare_es = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/compare_es' }),
  schema: articleSchema,
});

// Italian (it)
const blog_it = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog_it' }),
  schema: blogSchema,
});
const glossary_it = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/glossary_it' }),
  schema: glossarySchema,
});
const reviews_it = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/reviews_it' }),
  schema: articleSchema,
});
const alternatives_it = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/alternatives_it' }),
  schema: articleSchema,
});
const best_it = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/best_it' }),
  schema: articleSchema,
});
const compare_it = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/compare_it' }),
  schema: articleSchema,
});

// Portuguese Brazil (pt-br)
const blog_ptbr = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog_ptbr' }),
  schema: blogSchema,
});
const glossary_ptbr = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/glossary_ptbr' }),
  schema: glossarySchema,
});
const reviews_ptbr = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/reviews_ptbr' }),
  schema: articleSchema,
});
const alternatives_ptbr = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/alternatives_ptbr' }),
  schema: articleSchema,
});
const best_ptbr = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/best_ptbr' }),
  schema: articleSchema,
});
const compare_ptbr = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/compare_ptbr' }),
  schema: articleSchema,
});

export const collections = {
  // English
  reviews, alternatives, best, glossary, compare, blog,
  // German
  blog_de, glossary_de, reviews_de, alternatives_de, best_de, compare_de,
  // French
  blog_fr, glossary_fr, reviews_fr, alternatives_fr, best_fr, compare_fr,
  // Spanish
  blog_es, glossary_es, reviews_es, alternatives_es, best_es, compare_es,
  // Italian
  blog_it, glossary_it, reviews_it, alternatives_it, best_it, compare_it,
  // Portuguese Brazil
  blog_ptbr, glossary_ptbr, reviews_ptbr, alternatives_ptbr, best_ptbr, compare_ptbr,
};
