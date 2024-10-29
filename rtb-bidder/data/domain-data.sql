SET @new_company_name = 'RTB_BIDDER_Regression_Test';
SET @old_company_name = 'Column6';

INSERT INTO domain.company (
	guid, name, status, version, created_at, updated_at, primary_color, accent_color,
	button_color, logo_object_key, logo_file_name, logo_file_extension, email_logo_object_key,
	email_logo_file_name, email_logo_file_extension, favicon_object_key, favicon_file_name,
	favicon_file_extension, rpt_limit_rtb_dimensions, rpt_limit_rtb_range,
	rpt_limit_network_dimensions, rpt_limit_network_range, rpt_limit_campaign_dimensions,
	rpt_limit_campaign_range, rpt_limit_publisher_dimensions, rpt_limit_publisher_range,
	show_help_text, privacy_policy_url, t_c_url, default_rev_share, default_margin,
	forced_brand_safety, root_domain, arena_domain, mobile_domain, event_domain, rtb_domain,
	cookie_domain, publisher_domain, manage_domain, media_domain, cdn_domain, support_email,
	reporting_email, force_demand_bundle, default_marketplace_priority,
	default_marketplace_weight, send_ad_attempts, default_rtb_margin, company_domain,
	seller_type, managed_by_type, is_confidential, is_managing_ads_txt, allow_ivt_filtering,
	ivt_probability_threshold, enforce_ivt_filtering
)
SELECT
	'RMEVV0IKMD3HL7FVG9AB6LOQHS', @new_company_name, status, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, primary_color, accent_color,
	button_color, logo_object_key, logo_file_name, logo_file_extension, email_logo_object_key,
	email_logo_file_name, email_logo_file_extension, favicon_object_key, favicon_file_name,
	favicon_file_extension, rpt_limit_rtb_dimensions, rpt_limit_rtb_range,
	rpt_limit_network_dimensions, rpt_limit_network_range, rpt_limit_campaign_dimensions,
	rpt_limit_campaign_range, rpt_limit_publisher_dimensions, rpt_limit_publisher_range,
	show_help_text, privacy_policy_url, t_c_url, default_rev_share, default_margin,
	forced_brand_safety, root_domain, arena_domain, mobile_domain, event_domain, rtb_domain,
	cookie_domain, publisher_domain, manage_domain, media_domain, cdn_domain, support_email,
	reporting_email, force_demand_bundle, default_marketplace_priority,
	default_marketplace_weight, send_ad_attempts, default_rtb_margin, concat(@new_company_name, '.com'),
	seller_type, managed_by_type, is_confidential, is_managing_ads_txt, allow_ivt_filtering,
	ivt_probability_threshold, enforce_ivt_filtering
FROM domain.company
WHERE company.name = @old_company_name;

INSERT INTO domain.`user`
(`email`, `password`, `guid`, `first_name`, `last_name`, `company_id`, `time_zone`, `status`, `created_at`,
 `updated_at`)
SELECT 'rtb_bidder@column6.com', '$2a$10$xOROT705Dg.h6Jyh/6igTeGwncpkpB52PmkAOnrXCcBWKqHcy/efq',
		'3ISI2EKGCL511E917A86B6GG20', 'RTB_BIDDER_Automation_User', '',
		company.id, 'Z', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM domain.company
WHERE company.name = @new_company_name;

insert into user_advertiser (user_id, company_id, advertiser_id)
SELECT u.id, u.company_id,null
from user u
where u.email = 'rtb_bidder@column6.com';

insert into user_publisher (user_id, company_id, publisher_id)
SELECT u.id, u.company_id,null
from user u
where u.email = 'rtb_bidder@column6.com';


INSERT INTO domain.role ( company_id, name, description, created_at, updated_at)
select company.id, 'RTB_TEST_ADMIN', 'RTB TEST ADMIN', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM domain.company
WHERE company.name = @new_company_name;


-- Step 1: Get the role_id for the given role name
SET @new_role_name = 'RtbBidder Automation permissions';

-- Step 2: create new role
INSERT INTO domain.role (company_id, name, description, created_at, updated_at)
SELECT company.id, @new_role_name, @new_role_name, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM domain.company
WHERE company.name = @new_company_name;

-- Step 3: associate all role permissions to new role
SELECT id INTO @new_role_id
FROM domain.role
WHERE role.name = @new_role_name;

INSERT IGNORE INTO domain.role_permission (role_id, permission_id)
SELECT @new_role_id, permission_id
FROM domain.role_permission;

-- Step 4: associate new role to new user
insert into user_role (user_id, role_id)
select u.id, r.id
from user u,
	 role r
where u.email = 'rtb_bidder@column6.com'
  and r.id = @new_role_id;
