import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://thestacc.com',
  trailingSlash: 'always',
  image: { service: { entrypoint: 'astro/assets/services/noop' } },
});
