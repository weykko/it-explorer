document.addEventListener("DOMContentLoaded", function () {
    const loadingDiv = document.getElementById("loading");
    const vacanciesContainer = document.getElementById("vacancies-container");

    fetch(apiUrl)
        .then((response) => response.json())
        .then((data) => {
            loadingDiv.style.display = "none";
            vacanciesContainer.style.display = "block";

            const vacancies = data.vacancies;
            if (vacancies.length === 0) {
                vacanciesContainer.innerHTML = "<p>Нет вакансий за последние 24 часа.</p>";
            } else {
                vacanciesContainer.innerHTML = vacancies
                    .map(
                        (vacancy) => `
                    <section class="vacancy">
                        <div class="vacancy-header">
                            <h2 class="vacancy-title">${vacancy.name}</h2>
                            <p class="vacancy-salary">${vacancy.salary}</p>
                        </div>
                        <p class="vacancy-company">${vacancy.company}, ${vacancy.region}</p>
                        <p class="vacancy-skills">${vacancy.skills}</p>
                        <p class="vacancy-description">${vacancy.description}</p>
                        <div class="vacancy-footer">
                            <p class="vacancy-date">Дата публикации: ${vacancy.published_at}</p>
                        </div>
                    </section>
                `
                    )
                    .join("");
            }
        })
        .catch((error) => {
            loadingDiv.innerHTML = "<p>Ошибка загрузки вакансий. Попробуйте позже.</p>";
        });
});