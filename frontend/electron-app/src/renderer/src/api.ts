// 创建一个通用的 API 请求函数
const apiRequest = async (method: string, endpoint: string, data?: unknown) => {
  try {
    const response = await (window.api as any).apiRequest(method, `${endpoint}`, data)
    console.log(response)
    return response
  } catch (error) {
    // console.error('API request failed:', error)
  }
}

export const login = (credentials: { username: string; password: string }) =>
  apiRequest('POST', '/login', credentials)

export const register = (userData: { username: string; password: string }) =>
  apiRequest('POST', '/register', userData)

export const logout = () => apiRequest('GET', '/logout')

export const getTodos = () => apiRequest('GET', '/todos')

export const addTodo = (todo: { title: string; description: string; priority: number }) =>
  apiRequest('POST', '/todo', todo)

export const updateTodo = (
  id: number,
  todo: { title: string; description: string; status: boolean; priority: number }
) => apiRequest('PUT', `/todo/${id}`, todo)

export const deleteTodo = (id: number) => apiRequest('DELETE', `/todo/${id}`)
