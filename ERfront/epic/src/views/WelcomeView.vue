<template>
    <div class="character-creation">
      <!-- Приветствие -->
      <h1>Пафосный текст</h1>
      <p>Надо придумать что нибудь по-круче</p>
  
      <!-- Форма создания персонажа -->
      <form @submit.prevent="createCharacter" class="creation-form">
        <!-- Имя персонажа -->
        <label for="name">Имя персонажа:</label>
        <input
          type="text"
          id="name"
          v-model.trim="characterName"
          placeholder="Введите имя"
          required
        />
  
        <!-- Выбор класса -->
        <div class="class-selection">
          <h3>Выберите класс:</h3>
          <div class="class-buttons">
            <button
              v-for="cls in availableClasses"
              :key="cls.type"
              type="button"
              :class="['class-btn', { active: selectedClass?.type === cls.type }]"
              @click="selectClass(cls)"
            >
              {{ cls.label }}
            </button>
          </div>
        </div>
  
        <!-- Описание класса -->
        <div v-if="selectedClass" class="class-description">
          <h4>Описание класса: {{ selectedClass.label }}</h4>
          <p>{{ selectedClass.description }}</p>
        </div>
  
        <!-- Кнопка отправки -->
        <button type="submit" class="submit-btn" :disabled="!isFormValid">
          Создать персонажа
        </button>
      </form>
    </div>
</template>

<script>
export default {
    name: 'CreateCharacter',
    data() {
      return {
        characterName: '',
        selectedClass: null,
        availableClasses: [
          {
            type: 'warrior',
            label: 'воин',
            description: 'Сильный и выносливый боец, мастер владения мечом и щитом.'
          },
          {
            type: 'mage',
            label: 'маг',
            description: 'Обладатель древней мудрости и могущественных заклинаний.'
          }
        ],
      }
    },

    computed: {
      isFormValid() {
        return this.characterName && this.selectedClass
      }
    },

    methods: {
      selectClass(cls) {
        this.selectedClass = cls
      },

      async createCharacter() {
        if (!this.isFormValid) return

        try {
          const tg_user = window.Telegram.WebApp.initDataUnsafe?.user
          const response = await fetch(`http://127.0.0.1:8000/api/createChar`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              tg_id: tg_user.id,
              nickname: this.characterName,
              charClass: this.selectedClass.label
            })
          })
          this.$router.replace('/')
        } catch (error) {
            console.log(error)
        }
      }
    }
  }
</script>

<style scoped>
.character-creation {
  flex: 1;
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  font-family: Arial, sans-serif;
}

.creation-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

input[type='text'] {
  padding: 0.5rem;
  font-size: 1rem;
}

.class-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.class-btn {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #fff;
  transition: all 0.2s ease-in-out;
}

.class-btn.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.class-description {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #eef2f3;
  border-left: 4px solid #007bff;
}

.submit-btn {
  margin-top: 1rem;
  padding: 0.75rem;
  font-size: 1.1rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

.submit-btn:hover {
  background-color: #218838;
}

.submit-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>