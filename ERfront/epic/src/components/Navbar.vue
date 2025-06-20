<template>
	<nav class="navbar">
		<router-link to="/" class="nav-link">Задачи</router-link>
		<router-link to="/profile" class="nav-link">Профиль</router-link>
    <router-link to="/dungeon" class="nav-link">Подземелье</router-link>
    <router-link to="/guild" class="nav-link">Гильдия</router-link>
	</nav>
</template>

<script>
	export default{
		name:"Navbar"
	}
</script>

<style scoped>
.navbar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: calc(60px + env(safe-area-inset-bottom)); /* Для мобильных */
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-top: 1px solid #a97d5a;
  padding: 10px 0;
  z-index: 1000;
}

.nav-link {
  flex: 1;
  text-align: center;
  text-decoration: none;
  color: #5a3e2b;
  font-size: 14px;
  font-weight: bold;
  line-height: 1.2;
  transition: all 0.2s ease;
  position: relative;
}

/* Эффект "магической печати" при активной ссылке */
.nav-link.router-link-active::after {
  content: '';
  display: block;
  width: 30%;
  height: 3px;
  margin: 4px auto 0;
  background: radial-gradient(circle, #ffaa00, #cc7722);
  border-radius: 2px;
} 
</style>