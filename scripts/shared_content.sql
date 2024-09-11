-- Grant usage to a external database from the application.

USE APPLICATION PACKAGE {{package_name}};
CREATE SCHEMA IF NOT EXISTS shared_data;
USE SCHEMA shared_data;

grant reference_usage on database ML_APP
    to share in application package {{ package_name }};

-- Create a view that references the provider table.
-- The view is going to be shared by the package to the application.
create view if not exists shared_data.NAV_DATA
  as select * from ML_APP.ML_MODELS.NAV_DATA ORDER BY DATE DESC LIMIT 10;

grant usage on schema shared_data
  to share in application package {{ package_name }};
grant select on view shared_data.NAV_DATA
  to share in application package {{ package_name }};


