export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');

  const BASE_OFFSET = 380; // Base offset representing historical visits

  try {
    const apiRes = await fetch('https://api.counterapi.dev/v1/lunar-saas/visits/up');
    if (!apiRes.ok) {
      return res.status(200).json({ value: BASE_OFFSET + 15, error: `API status ${apiRes.status}` });
    }
    const data = await apiRes.json();
    
    // CounterAPI returns the count in data.count (not data.value)
    const totalVisits = (data.count || 0) + BASE_OFFSET;
    
    return res.status(200).json({ value: totalVisits });
  } catch (error) {
    console.error("Fetch error in serverless counter:", error);
    return res.status(200).json({ value: BASE_OFFSET + 15, error: error.message });
  }
}
