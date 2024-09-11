
CREATE APPLICATION ROLE IF NOT EXISTS invstintl_app_role;


CREATE OR ALTER VERSIONED SCHEMA code_schema;
GRANT USAGE ON SCHEMA code_schema TO APPLICATION ROLE invstintl_app_role;


CREATE VIEW IF NOT EXISTS code_schema.NAV_DATA
  AS SELECT *
  FROM shared_data.NAV_DATA;
GRANT SELECT ON VIEW code_schema.NAV_DATA TO APPLICATION ROLE invstintl_app_role;

create or replace procedure code_schema.update_reference(ref_name string, operation string, ref_or_alias string)
returns string
language sql
as $$
begin
  case (operation)
    when 'ADD' then
       select system$set_reference(:ref_name, :ref_or_alias);
    when 'REMOVE' then
       select system$remove_reference(:ref_name, :ref_or_alias);
    when 'CLEAR' then
       select system$remove_all_references(:ref_name);
    else
       return 'Unknown operation: ' || operation;
  end case;
  return 'Success';
end;
$$;

grant usage on procedure code_schema.update_reference(string, string, string) to application role invstintl_app_role;


CREATE STREAMLIT IF NOT EXISTS code_schema.investintel
  FROM '/streamlit'
  MAIN_FILE = '/investintel.py'
;

GRANT USAGE ON STREAMLIT code_schema.investintel TO APPLICATION ROLE invstintl_app_role;