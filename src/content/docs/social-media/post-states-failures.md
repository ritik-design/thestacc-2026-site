---
title: Post States & Failures
---

 <p>Every social post moves through a few states as theStacc generates its caption and image. Most of the time you will only ever see two of them: the post is ready, or it is published. But generation involves an AI writing engine and an AI image engine, and occasionally one of those steps does not finish. When that happens, theStacc tells you exactly what went wrong and gives you a single button to fix it.</p>
<p>This page lists every state a post can be in, the message you will see, and what to do next.</p>
<h2 id="where-you-see-the-state">Where you see the state<a aria-label="Copy link to Where you see the state" class="heading-anchor" href="#where-you-see-the-state">#</a></h2>
<p>Open any post from the calendar or the post list to reach its detail page. If a post needs your attention, a colored <strong>state banner</strong> appears at the top of that page, above the post content. The banner has three parts:</p>
<ul><li>An icon and color that match the severity (green for OK, blue for in progress, amber for a warning, red for an error).</li><li>A short, plain-language message explaining what happened.</li><li>A single action button, where one makes sense, that runs the fix for you.</li></ul>
<p>When you click the button, theStacc kicks off the fix and the page refreshes itself so the banner updates to the new state. You do not have to reload.</p>
<p>The banner only shows up when it is genuinely useful - for catastrophic failures and for posts that are still generating. For smaller issues, such as just the image failing, the fix lives right next to the thing that needs fixing instead (for example, a <strong>Generate image</strong> button under the empty image slot). So a post with no banner is not necessarily a post with no issue - always glance at the image and caption sections too.</p>
<h2 id="the-healthy-states">The healthy states<a aria-label="Copy link to The healthy states" class="heading-anchor" href="#the-healthy-states">#</a></h2>
<h3 id="ready">Ready<a aria-label="Copy link to Ready" class="heading-anchor" href="#ready">#</a></h3>
<p>The caption and image both generated successfully. The banner is green and reads:</p>
<blockquote><p>Post is ready to review.</p></blockquote>
<p>There is nothing to fix. Review the caption and image, then approve or publish the post. (Because this state is healthy and the status badge already says so, theStacc usually does not draw a separate banner for it - the post simply appears ready.)</p>
<h3 id="ready-with-warnings">Ready with warnings<a aria-label="Copy link to Ready with warnings" class="heading-anchor" href="#ready-with-warnings">#</a></h3>
<p>The post generated fine, but one or more of its captions is longer than a platform allows (for example, an X caption over the character limit). The post will not publish cleanly until you trim it. The message reads:</p>
<blockquote><p>Post is generated, but one or more captions exceed platform limits. Edit before publishing.</p></blockquote>
<p><strong>What to do:</strong> Edit the caption for the flagged platform and shorten it. The per-platform caption editor shows you the exact character count and limit for each platform, so you can see precisely how much to cut. Once you are under the limit, the warning clears.</p>
<h3 id="published">Published<a aria-label="Copy link to Published" class="heading-anchor" href="#published">#</a></h3>
<p>The post has already gone out to your connected platforms. The message reads:</p>
<blockquote><p>Post has been published.</p></blockquote>
<p>This is a settled, final state. There is nothing to act on here.</p>
<h3 id="in-progress">In progress<a aria-label="Copy link to In progress" class="heading-anchor" href="#in-progress">#</a></h3>
<p>Generation is actively running. The banner is blue with a spinning icon and reads:</p>
<blockquote><p>Generating... this usually takes 30-90 seconds.</p></blockquote>
<p><strong>What to do:</strong> Wait. The page polls in the background and updates itself the moment generation finishes - you do not need to refresh. This covers posts that are actively generating, publishing, or queued to run.</p>
<h2 id="the-failure-states">The failure states<a aria-label="Copy link to The failure states" class="heading-anchor" href="#the-failure-states">#</a></h2>
<p>When something goes wrong, theStacc does not just say "failed." It looks at what is actually on the post - whether the caption is there, whether an image is there, and which step broke - and gives you the most specific message and the right fix. Here is every failure type.</p>
<h3 id="total-failure">Total failure<a aria-label="Copy link to Total failure" class="heading-anchor" href="#total-failure">#</a></h3>
<p>Neither the caption nor the image generated. This usually means the AI service was briefly overloaded when your post tried to generate. The banner is red and reads:</p>
<blockquote><p>Couldn't generate this post. The AI service may be temporarily overloaded - please try again.</p></blockquote>
<p><strong>What to do:</strong> Click <strong>Try again</strong>. This re-runs the full generation from scratch. Overload errors are almost always temporary, so a retry a minute or two later usually succeeds.</p>
<h3 id="image-failed-only">Image failed only<a aria-label="Copy link to Image failed only" class="heading-anchor" href="#image-failed-only">#</a></h3>
<p>The caption generated successfully, but the image step did not produce an image - so the post has writing but no picture. The message reads:</p>
<blockquote><p>Caption is ready, but the image couldn't be generated. Try generating just the image again.</p></blockquote>
<p><strong>What to do:</strong> Click <strong>Generate image</strong>. theStacc keeps your finished caption and re-runs only the image step, so you are not paying for or waiting on a full regeneration. Your caption is untouched.</p>
<p>This is one of the states that often shows its fix inline (a <strong>Generate image</strong> button under the empty image slot) rather than as a top banner. Either way, the action is the same.</p>
<h3 id="caption-failed-only">Caption failed only<a aria-label="Copy link to Caption failed only" class="heading-anchor" href="#caption-failed-only">#</a></h3>
<p>The reverse situation - an image is attached, but the caption came back empty. The message reads:</p>
<blockquote><p>Image is ready, but the caption couldn't be generated. Try regenerating the caption.</p></blockquote>
<p><strong>What to do:</strong> Click <strong>Regenerate caption</strong> to re-run generation for this post.</p>
<h3 id="text-only-failed">Text-only failed<a aria-label="Copy link to Text-only failed" class="heading-anchor" href="#text-only-failed">#</a></h3>
<p>Some post formats are text-only by design - they never produce an image. When one of those fails, theStacc gives you a format-specific message rather than the generic one, so you are not left wondering where the missing image is:</p>
<blockquote><p>Text generation failed for this post. Please try again.</p></blockquote>
<p><strong>What to do:</strong> Click <strong>Try again</strong> to re-run generation. (See <a href="/docs/social-media/image-generation/">Image Generation</a> for which formats are text-only and therefore never carry an image.)</p>
<h3 id="worker-died-reaped">Worker died / reaped<a aria-label="Copy link to Worker died / reaped" class="heading-anchor" href="#worker-died-reaped">#</a></h3>
<p>The generation job started but the worker handling it stopped before finishing - usually an infrastructure hiccup rather than anything wrong with your post. theStacc detects this and marks the post as failed. The message reads:</p>
<blockquote><p>Generation worker stopped before finishing. Please try again.</p></blockquote>
<p><strong>What to do:</strong> Click <strong>Try again</strong>. A fresh run will normally pick up a healthy worker and complete.</p>
<h3 id="stuck-generating">Stuck generating<a aria-label="Copy link to Stuck generating" class="heading-anchor" href="#stuck-generating">#</a></h3>
<p>A post that has been sitting in the generating state for more than 25 minutes is treated as stuck - the worker almost certainly crashed without reporting it. Rather than leave the page spinning forever, theStacc surfaces this so you can recover. The banner is red and reads:</p>
<blockquote><p>Generation has been stuck for more than 25 minutes - the worker likely crashed. Please try again.</p></blockquote>
<p><strong>What to do:</strong> Click <strong>Try again</strong> to start a clean run. (Behind the scenes, theStacc also sweeps and clears these stuck posts automatically, but the banner lets you act immediately instead of waiting.)</p>
<h3 id="other-failures">Other failures<a aria-label="Copy link to Other failures" class="heading-anchor" href="#other-failures">#</a></h3>
<p>If a post fails in a way that does not match any of the patterns above, theStacc still does not leave you stranded. It shows a generic message:</p>
<blockquote><p>Generation failed. Please try again.</p></blockquote>
<p><strong>What to do:</strong> Click <strong>Try again</strong>.</p>
<h2 id="what-the-image-step-can-produce">What the image step can produce<a aria-label="Copy link to What the image step can produce" class="heading-anchor" href="#what-the-image-step-can-produce">#</a></h2>
<p>The state of a post is driven largely by what happened during image generation. There are exactly three outcomes for the image step:</p>
<ul><li><strong>Success</strong> - an image was generated and attached. The post can become <strong>Ready</strong>.</li><li><strong>Failed</strong> - the image step ran but produced zero images (for example, the image provider had an outage). For formats that are supposed to have a picture, the post is marked failed rather than quietly looking ready, so you never accidentally publish a post with a blank image slot. This is what produces the <strong>Image failed only</strong> state.</li><li><strong>Skipped</strong> - the post is a text-only format that is not meant to have an image at all. An empty image slot here is intentional, not a failure.</li></ul>
<p>That last distinction is why theStacc separates <strong>Text-only failed</strong> from <strong>Image failed only</strong>: a missing image on a text format is normal, but a missing image on an image format is a problem to fix. For more on how images are created, sized for each platform, and branded with your logo, see <a href="/docs/social-media/image-generation/">Image Generation</a>.</p>
<h2 id="editing-an-image-without-double-firing">Editing an image without double-firing<a aria-label="Copy link to Editing an image without double-firing" class="heading-anchor" href="#editing-an-image-without-double-firing">#</a></h2>
<p>When you refine an image with an instruction (for example, "make the background warmer"), the edit runs as a background job that can take around a minute and a half. While it is running, theStacc locks the controls so you cannot accidentally start a second, conflicting edit on the same image.</p>
<p>Concretely, while an image edit is in progress:</p>
<ul><li>The refine prompt box, the <strong>Refine</strong> button, and the reference options are all disabled.</li><li>The button shows <strong>Refining...</strong> with a spinner so you know the edit is still working.</li><li>A second click - or pressing Enter again - does nothing until the current edit finishes.</li></ul>
<p>When the edit completes, theStacc swaps the new image in place and confirms it. If the edit fails or times out, the controls unlock and you get a clear message so you can try again. This guard means one edit instruction equals exactly one edit - no duplicate runs, no wasted generation, and no race between two edits fighting over the same picture.</p>
<p>Image regeneration (generating a brand-new image rather than editing the current one) is guarded the same way. If a regeneration is already running for a post, theStacc blocks a second one and shows a "regenerating, please wait" state with a live timer, so you wait for the first run instead of starting a duplicate.</p>
<h2 id="a-quick-map-of-states-to-actions">A quick map of states to actions<a aria-label="Copy link to A quick map of states to actions" class="heading-anchor" href="#a-quick-map-of-states-to-actions">#</a></h2>
<div class="table-wrap"><table><thead><tr><th>State</th><th>What it means</th><th>Button</th></tr></thead><tbody><tr><td>Ready</td><td>Caption and image both succeeded</td><td>(none - review and publish)</td></tr><tr><td>Ready with warnings</td><td>A caption is over a platform's limit</td><td>Edit caption</td></tr><tr><td>In progress</td><td>Still generating</td><td>(none - wait)</td></tr><tr><td>Published</td><td>Already live</td><td>(none)</td></tr><tr><td>Image failed only</td><td>Caption is ready, image is missing</td><td>Generate image</td></tr><tr><td>Caption failed only</td><td>Image is ready, caption is missing</td><td>Regenerate caption</td></tr><tr><td>Text-only failed</td><td>A text-only post failed to generate</td><td>Try again</td></tr><tr><td>Total failure</td><td>Both caption and image failed</td><td>Try again</td></tr><tr><td>Worker died / reaped</td><td>The job stopped before finishing</td><td>Try again</td></tr><tr><td>Stuck generating</td><td>Stuck for more than 25 minutes</td><td>Try again</td></tr><tr><td>Other failure</td><td>An unclassified failure</td><td>Try again</td></tr></tbody></table></div>
<h2 id="related">Related<a aria-label="Copy link to Related" class="heading-anchor" href="#related">#</a></h2>
<ul><li><a href="/docs/social-media/content-plans-generation/">Content Plans &amp; Generation</a> - how posts get created and what each generation step does.</li><li><a href="/docs/social-media/image-generation/">Image Generation</a> - how images are produced, sized per platform, branded, and which formats are text-only.</li></ul> 