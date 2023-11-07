-- Создание таблицы для записи времени, когда значение больше 9
CREATE TABLE public."data" (
	"time" timestamp NULL,
	value int4 NULL,
	id int4 NULL
);

CREATE TABLE public.onemore (
	"time" timestamp NULL,
	value int4 NULL
);

CREATE OR REPLACE VIEW public.aggregated_data
AS SELECT date_trunc('minute'::text, data."time") AS time_minute,
    count(*) AS count,
    avg(data.value) AS average_value
   FROM data
  GROUP BY (date_trunc('minute'::text, data."time"));