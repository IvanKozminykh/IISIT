; =============================================================
;  ПРОЕКТ: Экспертная система выбора видеокарты RTX
;  Полностью совместима со стандартным CLIPS (6.x)
;  Версия: полная, 13 вопросов + 18 правил
; =============================================================

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Deffacts: начальные факты (инициализируются при загрузке)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Deffunctions: простые функции опроса (каждая для своего факта)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; --- Числовые вопросы ---

; Получаем значение пропускной шины 
(deffunction ask-bandwidth-increased ()
  (printout t "Введите значение пропускной шины в битах (например, 256): " )
  (bind ?v (read))
  (if (integerp ?v) then
    (assert (bandwidth-increased ?v))
    (printout t "[введено] bandwidth-increased " ?v crlf)
  else
    (printout t "Ошибка: ожидается целое число." crlf)
    (ask-bandwidth-increased)
  )
)

; Получаем значение пропускной способности
(deffunction ask-maximum-throughput-increased ()
  (printout t "Введите максимальную пропускную способность, например 1000 Гбайт/сек: ")
  (bind ?v (read))
  (if (integerp ?v) then
    (assert (maximum-throughput-increased ?v))
    (printout t "[введено] maximum-throughput-increased " ?v crlf)
  else
    (printout t "Ошибка: ожидается целое число." crlf)
    (ask-maximum-throughput-increased)
  )
)

; Получаем значение скорости оборота вентиляторов
(deffunction ask-high-fan-speed ()
  (printout t "Введите скорость оборотов вентиляторов (например 3200): ")
  (bind ?v (read))
  (if (integerp ?v) then
    (assert (high-fan-speed ?v))
    (printout t "[введено] high-fan-speed " ?v crlf)
  else
    (printout t "Ошибка: ожидается целое число." crlf)
    (ask-high-fan-speed)
  )
)

; Получаем количество вентиляторов
(deffunction ask-number-fans-increased ()
  (printout t "Введите количество вентиляторов (например 3): ")
  (bind ?v (read))
  (if (integerp ?v) then
    (assert (number-fans-increased ?v))
    (printout t "[введено] number-fans-increased " ?v crlf)
  else
    (printout t "Ошибка: ожидается целое число." crlf)
    (ask-number-fans-increased)
  )
)

; --- Булевые вопросы (yes/no) ---

(deffunction ask-memory-module-increased ()
  (printout t "Увеличен объем одного модуля памяти? (yes/no): ")
  (bind ?v (read))
  (if (or (eq ?v yes) (eq ?v no)) then
    (assert (memory-module-increased ?v))
    (printout t "[введено] memory-module-increased " ?v crlf)
  else
    (printout t "Введите 'yes' или 'no'." crlf)
    (ask-memory-module-increased)
  )
)

(deffunction ask-number-memory-modules-increased ()
  (printout t "Увеличенное количество модулей памяти? (yes/no): ")
  (bind ?v (read))
  (if (or (eq ?v yes) (eq ?v no)) then
    (assert (number-memory-modules-increased ?v))
    (printout t "[введено] number-memory-modules-increased " ?v crlf)
  else
    (printout t "Введите 'yes' или 'no'." crlf)
    (ask-number-memory-modules-increased)
  )
)

(deffunction ask-enlarged-radiators ()
  (printout t "Увеличенные радиаторы? (yes/no): ")
  (bind ?v (read))
  (if (or (eq ?v yes) (eq ?v no)) then
    (assert (enlarged-radiators ?v))
    (printout t "[введено] enlarged-radiators " ?v crlf)
  else
    (printout t "Введите 'yes' или 'no'." crlf)
    (ask-enlarged-radiators)
  )
)

(deffunction ask-evaporative-chamber ()
  (printout t "Присутствует испарительная камера? (yes/no): ")
  (bind ?v (read))
  (if (or (eq ?v yes) (eq ?v no)) then
    (assert (evaporative-chamber ?v))
    (printout t "[введено] evaporative-chamber " ?v crlf)
  else
    (printout t "Введите 'yes' или 'no'." crlf)
    (ask-evaporative-chamber)
  )
)

(deffunction ask-premium-brand ()
  (printout t "Премиальный бренд? (yes/no): ")
  (bind ?v (read))
  (if (or (eq ?v yes) (eq ?v no)) then
    (assert (premium-brand ?v))
    (printout t "[введено] premium-brand " ?v crlf)
  else
    (printout t "Введите 'yes' или 'no'." crlf)
    (ask-premium-brand)
  )
)

(deffunction ask-beautiful-performance ()
  (printout t "Красивое исполнение? (yes/no): ")
  (bind ?v (read))
  (if (or (eq ?v yes) (eq ?v no)) then
    (assert (beautiful-performance ?v))
    (printout t "[введено] beautiful-performance " ?v crlf)
  else
    (printout t "Введите 'yes' или 'no'." crlf)
    (ask-beautiful-performance)
  )
)

(deffunction ask-micro-atx-board ()
  (printout t "Micro-ATX плата? (yes/no): ")
  (bind ?v (read))
  (if (or (eq ?v yes) (eq ?v no)) then
    (assert (micro-atx-board ?v))
    (printout t "[введено] micro-atx-board " ?v crlf)
  else
    (printout t "Введите 'yes' или 'no'." crlf)
    (ask-micro-atx-board)
  )
)

(deffunction ask-reduced-case-size ()
  (printout t "Уменьшенный формат корпуса? (yes/no): ")
  (bind ?v (read))
  (if (or (eq ?v yes) (eq ?v no)) then
    (assert (reduced-case-size ?v))
    (printout t "[введено] reduced-case-size " ?v crlf)
  else
    (printout t "Введите 'yes' или 'no'." crlf)
    (ask-reduced-case-size)
  )
)

(deffunction ask-no-backlight ()
  (printout t "Отсутствие подсветки? (yes/no): ")
  (bind ?v (read))
  (if (or (eq ?v yes) (eq ?v no)) then
    (assert (no-backlight ?v))
    (printout t "[введено] no-backlight " ?v crlf)
  else
    (printout t "Введите 'yes' или 'no'." crlf)
    (ask-no-backlight)
  )
)

(deffunction ask-minimum-cooling-system-removal ()
  (printout t "Минимальная система охлаждения? (yes/no): ")
  (bind ?v (read))
  (if (or (eq ?v yes) (eq ?v no)) then
    (assert (minimum-cooling-system-removal ?v))
    (printout t "[введено] minimum-cooling-system-removal " ?v crlf)
  else
    (printout t "Введите 'yes' или 'no'." crlf)
    (ask-minimum-cooling-system-removal)
  )
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Правила: промежуточные признаки и выводы (всего 18)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 1) Увеличенный поток данных
(defrule r-increased-data-flow
  (declare (salience 4000))
  (bandwidth-increased ?a)
  (maximum-throughput-increased ?b)
  (test (or (>= ?a 512) (> ?b 1000)))
  =>
  (assert (increased-data-flow yes))
  (printout t "[r-increased-data-flow] increased-data-flow = yes" crlf)
)

; 2) Увеличенный размер модуля памяти
(defrule r-increased-memory-module-size
  (declare (salience 3900))
  (or
    (memory-module-increased yes)
    (number-memory-modules-increased yes)
  )
  =>
  (assert (increased-memory-module-size yes))
  (printout t "[r-increased-memory-module-size] increased-memory-module-size = yes" crlf)
)

; 3) Улучшенная система отвода тепла
(defrule r-improved-heat-dissipation-system
  (declare (salience 3800))
  (or
    (enlarged-radiators yes)
    (evaporative-chamber yes)
  )
  =>
  (assert (improved-heat-dissipation-system yes))
  (printout t "[r-improved-heat-dissipation-system] improved-heat-dissipation-system = yes" crlf)
)

; 4) Большая сила потока воздуха
(defrule r-high-air-flow-force
  (declare (salience 3700))
  (high-fan-speed ?a)
  (number-fans-increased ?b)
  (test (or (> ?a 2600) (> ?b 3)))
  =>
  (assert (high-air-flow-force yes))
  (printout t "[r-high-air-flow-force] high-air-flow-force = yes" crlf)
)

; 5) Повышенная стоимость компонентов
(defrule r-increased-cost-of-components
  (declare (salience 3600))
  (or
    (premium-brand yes)
    (beautiful-performance yes)
  )
  =>
  (assert (increased-cost-of-components yes))
  (printout t "[r-increased-cost-of-components] increased-cost-of-components = yes" crlf)
)

; 6) Компактность
(defrule r-compactness
  (declare (salience 3500))
  (micro-atx-board yes)
  (reduced-case-size yes)
  =>
  (assert (compactness yes))
  (printout t "[r-compactness] compactness = yes" crlf)
)

; 7) Слабовыраженные элементы
(defrule r-faintly-expressed-elements
  (declare (salience 3400))
  (no-backlight yes)
  =>
  (assert (faintly-expressed-elements yes))
  (printout t "[r-faintly-expressed-elements] faintly-expressed-elements = yes" crlf)
)

; 8) Минимальный набор компонентов
(defrule r-minimum-set-of-components
  (declare (salience 3300))
  (or
    (no-backlight yes)
    (minimum-cooling-system-removal yes)
  )
  =>
  (assert (minimum-set-of-components yes))
  (printout t "[r-minimum-set-of-components] minimum-set-of-components = yes" crlf)
)

;  9) Работа с ИИ
(defrule r-working-with-ai
  (declare (salience 3200))
  (increased-data-flow yes)
  (increased-memory-module-size yes)
  =>
  (assert (working-with-ai yes))
  (printout t "[r-working-with-ai] working-with-ai = yes" crlf)
)

; 10) Улучшеная система охлаждения
(defrule r-improved-cooling-system
  (declare (salience 3100))
  (improved-heat-dissipation-system yes)
  (high-air-flow-force yes)
  =>
  (assert (improved-cooling-system yes))
  (printout t "[r-improved-cooling-system] improved-cooling-system = yes" crlf)
)

; 11) Бюджет свыше 100к
(defrule r-budget-over-hight
  (declare (salience 3000))
  (increased-cost-of-components yes)
  =>
  (assert (budget-over-hight yes))
  (printout t "[r-budget-over-hight] budget-over-hight = yes" crlf)
)

; 12) Минималистичный вид
(defrule r-minimalistic-look
  (declare (salience 2900))
  (or 
    (increased-cost-of-components yes)
    (compactness yes)
    (faintly-expressed-elements yes)
  )
  =>
  (assert (minimalistic-look yes))
  (printout t "[r-minimalistic-look] minimalistic-look = yes" crlf)
)

; 13) Минимальная стоимость
(defrule r-minimum-cost
  (declare (salience 2800))
  (faintly-expressed-elements yes)
  (minimum-set-of-components yes)
  =>
  (assert (minimum-cost yes))
  (printout t "[r-minimum-cost] minimum-cost = yes" crlf)
)

; 14) RTX 5090
(defrule r-rtx-5090
  (declare (salience 100))
  (working-with-ai yes)
  (improved-cooling-system yes)
  (budget-over-hight yes)
  ?f <- (recommendation-made no)
  =>
  (retract ?f)
  (assert (recommendation RTX-5090))
  (assert (recommendation-made yes))
  (printout t "Рекомендация RTX-5090" crlf)
)

; 15) RTX 5080
(defrule r-rtx-5080
  (declare (salience 90))
  (improved-cooling-system yes)
  (budget-over-hight yes)
  ?f <- (recommendation-made no)
  =>
  (retract ?f)
  (assert (recommendation RTX-5080))
  (assert (recommendation-made yes))
  (printout t "Рекомендация RTX-5080" crlf)
)

; 16) RTX 5070Ti
(defrule r-rtx-5070-ti
  (declare (salience 80))
  (budget-over-hight yes)
  (minimalistic-look yes)
  ?f <- (recommendation-made no)
  =>
  (retract ?f)
  (assert (recommendation RTX-5070-ti))
  (assert (recommendation-made yes))
  (printout t "Рекомендация RTX-5070Ti" crlf)
)

; 17) RTX 5070
(defrule r-rtx-5070
  (declare (salience 70))
  (minimalistic-look yes)
  ?f <- (recommendation-made no)
  =>
  (retract ?f)
  (assert (recommendation RTX-5070))
  (assert (recommendation-made yes))
  (printout t "Рекомендация RTX-5070" crlf)
)

; 18) RTX 5060Ti
(defrule r-rtx-5060-ti
  (declare (salience 60))
  (minimalistic-look yes)
  (minimum-cost yes)
  ?f <- (recommendation-made no)
  =>
  (retract ?f)
  (assert (recommendation RTX-5060-ti))
  (assert (recommendation-made yes))
  (printout t "Рекомендация RTX-5060Ti" crlf)
)

; 19) RTX 5060
(defrule r-rtx-5060
  (declare (salience 50))
  (or
    (minimalistic-look yes)
    (minimum-cost yes)
  )
  ?f <- (recommendation-made no)
  =>
  (retract ?f)
  (assert (recommendation RTX-5060))
  (assert (recommendation-made yes))
  (printout t "Рекомендация RTX-5060" crlf)
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Запуск интерактивной сессии
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(deffunction run-session ()
  (reset)

  (assert (recommendation-made no))

  (printout t "=== Начинаем интерактивный опрос для выбора RTX ===" crlf)

  ;; Числовые параметры
  (ask-bandwidth-increased)
  (ask-maximum-throughput-increased)
  (ask-high-fan-speed)
  (ask-number-fans-increased)

  ;; Булевые параметры
  (ask-memory-module-increased)
  (ask-number-memory-modules-increased)
  (ask-enlarged-radiators)
  (ask-evaporative-chamber)
  (ask-premium-brand)
  (ask-beautiful-performance)
  (ask-micro-atx-board)
  (ask-reduced-case-size)
  (ask-no-backlight)
  (ask-minimum-cooling-system-removal)
  
  (printout t "--- FACTS BEFORE RUN ---" crlf)
  (facts)

  (printout t crlf "Запуск механизма вывода правил..." crlf)
  (run)
  
  (printout t "=== Конец сессии ===" crlf)
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Конец скрипта
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
