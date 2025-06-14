import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'

const app = createApp(App)
const pinia = createPinia()

if (window.Telegram?.WebApp) {
	window.Telegram.WebApp.ready();
	window.Telegram.WebApp.expand();
}

if (process.env.NODE_ENV === 'development') {
	window.Telegram = {
	  WebApp: {
		initDataUnsafe: {
		  user: {
			id: 1,
			first_name: 'Test1',
			username: 'test_user'
		  }
		}
	  }
	};
  }

app.use(router)
app.use(pinia)

app.mount('#app')
