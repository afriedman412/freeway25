target_pac_expenditures_per_target_candidate = """
SELECT fec_committee_id, fec_committee_name, fec_candidate_id, \
    candidate_name, office, state, district, sum(amount), count(*)
FROM fiu_pp
WHERE fec_committee_id IN (
    SELECT id FROM target_pacs
)
AND fec_candidate_id IN (
    SELECT candidate_id FROM candidates
)
GROUP BY fec_committee_id, fec_candidate_id
"""

topic_pac_donations_to_target_pacs = """
SELECT query_committee_id, query_committee_name, name, \
    contributor_id, contribution_receipt_amount, \
        contribution_receipt_date, transaction_id, file_number, sub_id
FROM donor_sked_a
INNER JOIN topic_pacs
ON donor_sked_a.contributor_id=topic_pacs.id
ORDER BY name, contribution_receipt_date
"""
