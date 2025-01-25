export function createSidebar() {
    const sidebarContainer = document.querySelector('.sidebar');

    const widget = document.createElement('ul');
    // widget.classList.add('weather-widget', 'start-widget', 'fade-in');
    // widget.id = 'start-widget'
    widget.innerHTML = `
        <li><a href="{% url 'home' %}" class="{% if request.path == '/' %}active{% endif %}">Главная</a></li>
        <li><a href="{% url 'general' %}" class="{% if request.path == '/general/' %}active{% endif %}">Общая статистика</a></li>
        <li><a href="{% url 'demand' %}" class="{% if request.path == '/demand/' %}active{% endif %}">Востребованность</a></li>
        <li><a href="{% url 'geography' %}" class="{% if request.path == '/geography/' %}active{% endif %}">География</a></li>
        <li><a href="{% url 'skills' %}" class="{% if request.path == '/skills/' %}active{% endif %}">Навыки</a></li>
        <li><a href="{% url 'latest_vacancies' %}" class="{% if request.path == '/latest_vacancies/' %}active{% endif %}">Последние вакансии</a></li>
    `;

    sidebarContainer.appendChild(widget);
    // widget.addEventListener('animationend', () => { widget.classList.remove('fade-in'); });
}

export function createSection() {
    const sidebarContainer = document.querySelector('.section-skills');

    const widget = document.createElement('div');
    // widget.classList.add('weather-widget', 'start-widget', 'fade-in');
    // widget.id = 'start-widget'
    widget.innerHTML = `
        <h2>{{ top_skills.title }}</h2>
        <div class="content-box-skills">
                {{ top_skills.table_data|safe }}
            <img src="{{ top_skills.graph.url }}" alt="{{ top_skills.title }}">
        </div>
    `;

    sidebarContainer.appendChild(widget);
    // widget.addEventListener('animationend', () => { widget.classList.remove('fade-in'); });
}