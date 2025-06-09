<template>
  <div class="app_container">

    <router-view />
    
    <Navbar />
  
  </div>
</template>

<script>
  import Navbar from './components/Navbar.vue'
  export default{
    name: 'App',
    components:{
      Navbar
    }
  }
</script>

<style scoped>
.app_container{
  display: flex;
  flex-direction: column;
  height: 98vh;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, sans-serif;
  background: linear-gradient(to bottom right, #f0f0f0, #ffffff);
}
</style>
