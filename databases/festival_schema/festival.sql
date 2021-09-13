-- PostgreSQL

CREATE TYPE "ticket_type" AS ENUM (
  'general_admission_one_day',
  'general_admission_all_days',
  'vip_one_day',
  'vip_all_days'
);

CREATE TYPE "staff_roles" AS ENUM (
  'security',
  'supervisor',
  'driver',
  'coordinator',
  'vendor',
  'audio_technician',
  'volunteer'
);

CREATE TABLE "locations" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "festivals" (
  "id" SERIAL PRIMARY KEY,
  "name" int,
  "starts_at" timestamp,
  "ends_at" timestamp,
  "location_id" int
);

CREATE TABLE "lineups" (
  "festival_id" int,
  "band_id" int,
  "start" timestamp,
  "end" timestamp
);

CREATE TABLE "bands" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "genres" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "band_genre" (
  "band_id" int,
  "genre_id" int
);

CREATE TABLE "participants" (
  "id" SERIAL PRIMARY KEY,
  "full_name" varchar,
  "email" varchar,
  "phone" varchar,
  "location_id" int
);

CREATE TABLE "attendees" (
  "participant_id" int,
  "festival_id" int,
  "ticket_id" int
);

CREATE TABLE "tickets" (
  "id" SERIAL PRIMARY KEY,
  "number" int,
  "participant_id" int,
  "price" int,
  "type" ticket_type
);

CREATE TABLE "staff" (
  "participant_id" int,
  "role" staff_roles
);

ALTER TABLE "participants" ADD FOREIGN KEY ("location_id") REFERENCES "locations" ("id");

ALTER TABLE "festivals" ADD FOREIGN KEY ("location_id") REFERENCES "locations" ("id");

ALTER TABLE "band_genre" ADD FOREIGN KEY ("band_id") REFERENCES "bands" ("id");

ALTER TABLE "band_genre" ADD FOREIGN KEY ("genre_id") REFERENCES "genres" ("id");

ALTER TABLE "staff" ADD FOREIGN KEY ("participant_id") REFERENCES "participants" ("id");

ALTER TABLE "attendees" ADD FOREIGN KEY ("participant_id") REFERENCES "participants" ("id");

ALTER TABLE "attendees" ADD FOREIGN KEY ("festival_id") REFERENCES "festivals" ("id");

ALTER TABLE "attendees" ADD FOREIGN KEY ("ticket_id") REFERENCES "tickets" ("id");

ALTER TABLE "lineups" ADD FOREIGN KEY ("band_id") REFERENCES "bands" ("id");

ALTER TABLE "lineups" ADD FOREIGN KEY ("festival_id") REFERENCES "festivals" ("id");
