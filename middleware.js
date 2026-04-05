export default async function middleware(request) {
  const url = new URL(request.url);
  const hostname = url.hostname;

  // Only handle subdomains of scortt.org
  if (!hostname.endsWith('.scortt.org')) return;

  const subdomain = hostname.slice(0, hostname.indexOf('.scortt.org'));
  if (subdomain === 'www') return;

  // Only rewrite root path — all other paths fall through to vercel.json rewrites
  if (url.pathname !== '/') return;

  const fileUrl = new URL(request.url);
  fileUrl.hostname = 'redbookveda.vercel.app';
  fileUrl.pathname = `/clients/${subdomain}/index.html`;

  const response = await fetch(fileUrl.toString());
  return new Response(response.body, {
    status: response.status,
    headers: { 'content-type': 'text/html; charset=utf-8' },
  });
}

export const config = {
  matcher: '/:path*',
};
