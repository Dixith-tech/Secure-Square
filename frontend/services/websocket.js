class WebSocketClient {
  constructor(url = "ws://127.0.0.1:8000/ws") {
    this.url = url;
    this.socket = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 3000;
    this.listeners = {};
  }

  connect() {
    return new Promise((resolve, reject) => {
      try {
        this.socket = new WebSocket(this.url);

        this.socket.onopen = () => {
          console.log('✓ WebSocket connected');
          this.reconnectAttempts = 0;
          this.emit('connect', { status: 'connected' });
          resolve(this.socket);
        };

        this.socket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            this.emit('message', data);
          } catch (e) {
            console.error('Failed to parse WebSocket message:', e);
          }
        };

        this.socket.onerror = (error) => {
          console.error('✗ WebSocket error:', error);
          this.emit('error', error);
          reject(error);
        };

        this.socket.onclose = () => {
          console.log('✗ WebSocket disconnected');
          this.emit('disconnect', { status: 'disconnected' });
          this.attemptReconnect();
        };
      } catch (error) {
        console.error('WebSocket connection failed:', error);
        reject(error);
      }
    });
  }

  send(data) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(data));
    } else {
      console.warn('WebSocket not connected');
    }
  }

  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(callback);
  }

  off(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
    }
  }

  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(callback => {
        callback(data);
      });
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      
      setTimeout(() => {
        this.connect().catch(err => {
          console.error('Reconnection failed:', err);
        });
      }, this.reconnectDelay);
    } else {
      console.error('Max reconnection attempts reached');
      this.emit('max_reconnect_attempts', {});
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }

  isConnected() {
    return this.socket && this.socket.readyState === WebSocket.OPEN;
  }
}

// Create and export singleton instance
const wsClient = new WebSocketClient();

export default wsClient;
export { WebSocketClient };
