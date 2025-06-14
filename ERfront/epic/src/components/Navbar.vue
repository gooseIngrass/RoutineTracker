<template>
	<nav class="navbar">
		<router-link to="/" class="nav-link">Задачи</router-link>
		<router-link to="/profile" class="nav-link">Профиль</router-link>
    <router-link to="/dungeon" class="nav-link">Подземелье</router-link>
    <router-link to="/city" class="nav-link">Город</router-link>
	</nav>
</template>

<script>
	export default{
		name:"Navbar"
	}
</script>

<style scoped>
.navbar{
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 60px;
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-top: 1px solid #ccc;
}

.nav-link{
  text-decoration: none;
  color: #333;
  font-size: 16px;
  font-weight: 500;
}
</style>