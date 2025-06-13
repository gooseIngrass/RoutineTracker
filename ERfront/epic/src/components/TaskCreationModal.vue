<template>
    <div class="modal-window">
        <p>{{ msg }}</p>
    </div>
</template>

<script>
    export default{
        name:"TaskCreationModal",
        props:{
            msg:String
        }
    }
</script>

<style scoped>
.modal-window {
  background-color: aquamarine;
  position: fixed;
  z-index: 999;
  top: 20%;
  left: 50%;
  width: 300px;
  margin-left: -150px;
}
</style>