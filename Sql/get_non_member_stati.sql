/*  File: Sql/get_non_member_stati_f.sql */
/*  Used by code.commands.get_stati_cmd */
SELECT
    P.personID, P.first, P.last, St.key
FROM 
    People AS P
JOIN
    Person_Status AS PS
ON 
    P.personID = PS.personID
JOIN
    Stati as St
ON
    St.statusID = PS.statusID
WHERE
    St.key IN  ("a-", "a" , "a0", "a1", "a2",
        "a3", "ai", "ad", "av", "aw", "am",
        "be", -- "Email on record being rejected",   # => special notice
        "ba", -- "Postal address => mail returned",  # => special notice
        "h",  -- Honorary Member",                             #10 > #12
--        "m",  -- Member in good standing",
        "i",  -- Inactive (continuing to receive minutes)",
        "r",  -- Retiring/Giving up Club Membership",
        "t",  -- Membership terminated (probably non payment of fees)",
                -- a not yet implemented temporary
                -- status to trigger a regret letter
        "w",  -- Fees being waived",  # a rarely applied special status
        "z1_pres", -- "President",
        "z2_vp", -- "VicePresident",
        "z3_sec", -- "Secretary of the Club",
        "z4_treasurer", -- "Treasurer",
        "z5_d_odd", -- "Director- term ends Feb next odd year",
        "z6_d_even", -- "Director- term ends Feb next even year",
        "zae", -- "Application expired or withdrawn",
        "zzz" -- "No longer a member"  # not implemented
    )
AND
    ( PS.end = '' OR PS.end > {} )
ORDER BY St.key
;
