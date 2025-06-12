import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

if (window.Telegram?.WebApp) {
	window.Telegram.WebApp.ready();
	window.Telegram.WebApp.expand();
}

if (process.env.NODE_ENV === 'development') {
	window.Telegram = {
	  WebApp: {
		initDataUnsafe: {
		  user: {
			id: 24,
			first_name: 'Test1',
			username: 'test_user'
		  }
		}
	  }
	};
  }

app.use(router)

app.mount('#app')
