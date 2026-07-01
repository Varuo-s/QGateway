const jsonHeaders = { Accept: "application/json" };

export async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(path, { headers: jsonHeaders });
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status} ${response.statusText}`);
  }
  return response.json() as Promise<T>;
}
