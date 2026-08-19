document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('taskInput');
    const addTaskBtn = document.getElementById('addTaskBtn');
    const taskList = document.getElementById('taskList');

    // Add task when button is clicked
    addTaskBtn.addEventListener('click', addTask);

    // Add task when Enter key is pressed
    taskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTask();
        }
    });

    function addTask() {
        const text = taskInput.value.trim();
        if (text === '') return;

        // Create elements
        const li = document.createElement('li');
        li.className = 'task-item';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'task-content';

        const checkbox = document.createElement('div');
        checkbox.className = 'checkbox';
        checkbox.innerHTML = '<i class="fas fa-check"></i>';

        const span = document.createElement('span');
        span.className = 'task-text';
        span.textContent = text;

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn';
        deleteBtn.innerHTML = '<i class="fas fa-trash"></i>';

        // Event Listeners for new task
        contentDiv.addEventListener('click', () => {
            li.classList.toggle('completed');
        });

        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent triggering the completion toggle
            li.classList.add('removing');
            // Wait for animation to finish before removing from DOM
            setTimeout(() => {
                li.remove();
            }, 300);
        });

        // Assemble
        contentDiv.appendChild(checkbox);
        contentDiv.appendChild(span);
        li.appendChild(contentDiv);
        li.appendChild(deleteBtn);
        
        // Add to list
        taskList.appendChild(li);

        // Clear input
        taskInput.value = '';
        taskInput.focus();
    }

    // Add a couple of initial tasks for demonstration
    taskInput.value = "Record LinkedIn video for CodSoft";
    addTask();
    taskInput.value = "Review Task 1 outputs";
    addTask();
});
