export async function onRequestPost(context) {
  const { REMOVE_BG_API_KEY } = context.env;
  
  if (!REMOVE_BG_API_KEY) {
    return new Response(JSON.stringify({ error: 'API key not configured' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });
  }

  try {
    const formData = await context.request.formData();
    const imageFile = formData.get('image_file');
    
    const removeBgResponse = await fetch('https://api.remove.bg/v1.0/removebg', {
      method: 'POST',
      headers: {
        'X-Api-Key': REMOVE_BG_API_KEY
      },
      body: formData
    });

    if (!removeBgResponse.ok) {
      return new Response(JSON.stringify({ error: 'API request failed' }), {
        status: removeBgResponse.status,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }

    const imageBlob = await removeBgResponse.blob();
    
    return new Response(imageBlob, {
      headers: {
        'Content-Type': 'image/png',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'no-cache'
      }
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });
  }
}
