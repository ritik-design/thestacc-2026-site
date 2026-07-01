import { defineConfig } from 'astro/config';

import cloudflare from "@astrojs/cloudflare";

export default defineConfig({
  site: 'https://thestacc.com',
  trailingSlash: 'always',
  image: { service: { entrypoint: 'astro/assets/services/noop' } },
  adapter: cloudflare()
});