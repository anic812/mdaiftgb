const HTML_TEMPLATE = `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <link rel="icon" type="image/x-icon" href="https://mediaarea.net//images/f060656-5397225.ico">
    <title>{{TITLE}}</title>
    <style>
      body {
        margin: 0;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
      }
      #particles-js {
        position: absolute;
        width: 100%;
        height: 100%;
        background-color: #2d3437;
      }
      .card {
        background-color: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(5px);
        position: relative;
        width: 70%;
        max-width: 500px;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        text-align: center;
      }
      .title {
        font-family: cursive;
        font-weight: bold;
        font-size: 25px;
        color: white;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
      }
      hr {
        width: 75%;
        margin: 20px auto;
      }
      img {
        max-width: 80%;
        height: auto;
        display: block;
        margin: 20px auto;
        border-radius: 8px;
      }
    </style>
  </head>
  <body>
    <div id="particles-js"></div>
    <div class="card">
      {{BODY_CONTENT}}
      <img src="https://www.pocketmonsters.net/images/pmwobba.png" alt="Wobbbuh!" />
    </div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
      particlesJS({
        particles: {
          number: { value: 600, density: { enable: true, value_area: 2600 } },
          color: { value: "#ffffff" },
          shape: {
            type: "triangle",
            stroke: { width: 5, color: "#254955" },
            polygon: { nb_sides: 12 },
          },
          opacity: {
            value: 0.49705773886831206,
            random: true,
            anim: { enable: false, speed: 1, opacity_min: 0.1, sync: false },
          },
          size: {
            value: 6,
            random: true,
            anim: { enable: true, speed: 40, size_min: 2.436231636904035, sync: true },
          },
          line_linked: {
            enable: true,
            distance: 150,
            color: "#ffffff",
            opacity: 0.4,
            width: 1,
          },
          move: {
            enable: true,
            speed: 20,
            direction: "none",
            random: true,
            straight: false,
            out_mode: "bounce",
            bounce: false,
            attract: { enable: true, rotateX: 600, rotateY: 1200 },
          },
        },
        interactivity: {
          detect_on: "canvas",
          events: {
            onhover: { enable: true, mode: "grab" },
            onclick: { enable: true, mode: "push" },
            resize: true,
          },
          modes: {
            grab: { distance: 400, line_linked: { opacity: 1 } },
            bubble: { distance: 400, size: 40, duration: 2, opacity: 8, speed: 3 },
            repulse: { distance: 200, duration: 0.4 },
            push: { particles_nb: 4 },
            remove: { particles_nb: 2 },
          },
        },
        retina_detect: true,
      });
    </script>
  </body>
</html>`;

const BODY_404 = `
  <div class="title">ERROR 404</div>
  <hr />
  <div class="title">Nothing was there</div>
`;

const BODY_DEFAULT = `
  <div class="title">Welcome</div>
  <hr />
  <div class="title">Nothing is here!!! ;)</div>
`;

function generateRandomString(length = 6) {
  const chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
  return Array.from({length}, () => chars[Math.floor(Math.random() * chars.length)]).join('');
}

async function saveData(data) {
  let key;
  do {
    key = generateRandomString();
  } while (await LINKS.get(key) !== null);
  
  await LINKS.put(key, data,{expirationTtl: 999999});
  return key;
}

function renderHTML(title, bodyContent) {
  return HTML_TEMPLATE
    .replace('{{TITLE}}', title)
    .replace('{{BODY_CONTENT}}', bodyContent);
}

async function handlePostRequest(request) {
  const { data } = await request.json();
  
  if (!data) {
    return new Response(JSON.stringify({ status: 400, message: 'Error: data is missing or invalid.' }), {
      status: 400,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  }

  try {
    const key = await saveData(data);
    return new Response(JSON.stringify({ status: 200, key: `/${key}` }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  } catch (error) {
    return new Response(JSON.stringify({ status: 500, message: 'Error: Failed to save data.' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  }
}

async function handleGetRequest(request) {
  const url = new URL(request.url);
  const path = url.pathname.slice(1);

  if (!path) {
    return new Response(renderHTML('Welcome', BODY_DEFAULT), {
      headers: { 'Content-Type': 'text/html;charset=UTF-8' },
    });
  }

  const value = await LINKS.get(path);
  if (value) {
    return new Response(value, {
      headers: { 'Content-Type': 'text/html;charset=UTF-8' },
    });
  }

  return new Response(renderHTML('404 - Not Found', BODY_404), {
    status: 404,
    headers: { 'Content-Type': 'text/html;charset=UTF-8' },
  });
}

async function handleRequest(request) {
  if (request.method === 'POST') {
    return handlePostRequest(request);
  } else if (request.method === 'GET') {
    return handleGetRequest(request);
  } else if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    });
  }

  return new Response('Method Not Allowed', { status: 405 });
}

addEventListener('fetch', (event) => {
  event.respondWith(handleRequest(event.request));
});