const API_BASE = '/api/v1'

export async function api(path, opts = {}) {
  const token = localStorage.getItem('token')
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...opts.headers
  }

  const url = `${API_BASE}${path}`
  const options = {
    ...opts,
    headers
  }

  try {
    const response = await fetch(url, options)
    
    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(errorText || `HTTP ${response.status}`)
    }

    const contentType = response.headers.get('content-type')
    if (contentType && contentType.includes('application/json')) {
      return await response.json()
    } else {
      return await response.text()
    }
  } catch (error) {
    console.error('API request failed:', error)
    throw error
  }
}

// Convenience methods
export const apiClient = {
  get: (path) => api(path, { method: 'GET' }),
  
  post: (path, data) => api(path, {
    method: 'POST',
    body: JSON.stringify(data)
  }),
  
  put: (path, data) => api(path, {
    method: 'PUT',
    body: JSON.stringify(data)
  }),
  
  delete: (path) => api(path, { method: 'DELETE' }),
  
  upload: (path, file) => {
    const formData = new FormData()
    formData.append('file', file)
    
    return api(path, {
      method: 'POST',
      headers: {}, // Let browser set content-type for FormData
      body: formData
    })
  }
}
