DROP TABLE IF EXISTS img_info;

CREATE TABLE img_info (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  img_color_contours TEXT,
  img_only_color TEXT,
  barcode_info TEXT,
  img_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);