export default async function middleware(request) {
  const url = new URL(request.url);
  const hostname = url.hostname;

  // Only handle subdomains of scortt.org
  if (!hostname.endsWith('.scortt.org')) return;

  const subdomain = hostname.slice(0, hostname.indexOf('.scortt.org'));
  if (subdomain === 'www') return;

  // Rewrite: xy.scortt.org/ → serve /clients/xy/index.html
  const filePath = `/clients/${subdomain}/index.html`;
  const fileUrl = new URL(filePath, request.url);

  const response = await fetch(fileUrl.toString());
  return new Response(response.body, {
    status: response.status,
    headers: { 'content-type': 'text/html; charset=utf-8' },
  });
}

export const config = {
  matcher: '/:path*',
};
