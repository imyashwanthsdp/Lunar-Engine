export default async function handler(req, res) {
  // Prevent browser and CDN caching of this endpoint
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');

  try {
    const response = await fetch('https://api.counterapi.dev/v1/lunar-saas/visits/up');
    if (!response.ok) {
      throw new Error(`CounterAPI returned status ${response.status}`);
    }
    const data = await response.json();
    return res.status(200).json({ value: data.value });
  } catch (error) {
    console.error('Error fetching CounterAPI in serverless function:', error);
    
    // Serverless fallback: return a reasonable base count
    // to prevent the UI from displaying an error
    return res.status(200).json({ value: 412, fallback: true });
  }
}
