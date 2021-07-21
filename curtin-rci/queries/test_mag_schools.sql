SELECT
    CASE
        WHEN
            OriginalAffiliation = "Curtin University"
            OR OriginalAffiliation = "Curtin University,Australia"
            OR OriginalAffiliation = "Curtin University, Australia"
            OR OriginalAffiliation = "Curtin Univ. of Technology (Australia)"
            OR OriginalAffiliation = "Curtin University,Bentley,Western Australia,Australia."
            OR OriginalAffiliation = "Curtin University  Perth WA"
            OR OriginalAffiliation = "1Curtin University, Perth, Australia"
            OR OriginalAffiliation = "Curtin Univ. of Technology, Perth, WA, Australia"
            OR OriginalAffiliation = "Curtin University of Technology , Perth, Western Australia, Australia"
            OR OriginalAffiliation = "Curtin University of Technology , Perth, Western Australia, Australia"
            OR OriginalAffiliation = "Curtin University, Kent Street, Bentley, WA 6102, Australia#TAB#"
            OR OriginalAffiliation = "Curtin University of Technology , Perth, Western Australia, Australia"
            OR OriginalAffiliation = "Curtin Univ. of Technol. ., Perth"
            OR OriginalAffiliation = "1 Curtin University, Perth, Western Australia, Australia."
            OR LOWER(OriginalAffiliation) like "curtin university%perth"
            OR LOWER(OriginalAffiliation) like "curtin university%perth%australia"
            OR LOWER(OriginalAffiliation) like "curtin university%perth%australia,"
            OR LOWER(OriginalAffiliation) like "curtin univ%bentley%australia"
            OR LOWER(OriginalAffiliation) = "curtin university of technology"
            OR LOWER(OriginalAffiliation) = "curtin#n#          university of technology"
            OR LOWER(OriginalAffiliation) = "curtin university of technology perth, australia#tab#"
                THEN null
        WHEN
            LOWER(OriginalAffiliation) like "%public health%"
            OR LOWER(OriginalAffiliation) like "%public heath%"
            OR LOWER(OriginalAffiliation) like "%population health%"
            OR LOWER(OriginalAffiliation) like "%psychology%"
            OR LOWER(OriginalAffiliation) like "%accident research centre%" -- C-MARC
                THEN "School of Population Health"
        WHEN
            LOWER(OriginalAffiliation) like "%allied health%"
            OR LOWER(OriginalAffiliation) like "%physiotherapy%"
            OR LOWER(OriginalAffiliation) like "%occupational therapy%"
                THEN "School of Allied Health"
        WHEN LOWER(OriginalAffiliation)
            like "%medical%"
            THEN "Curtin Medical School"
        WHEN
            LOWER(OriginalAffiliation) like "%curtin law%"
                THEN "Curtin Law School"
        WHEN
            LOWER(OriginalAffiliation) like "%civil%mechanical%"
            OR LOWER(OriginalAffiliation) like "%civil%engineering%"
            OR LOWER(OriginalAffiliation) like "%civil%engneering%"
            OR LOWER(OriginalAffiliation) like "%mech. eng.%"
            OR LOWER(OriginalAffiliation) like "%mechanical%engineering%"
            OR LOWER(OriginalAffiliation) like "%fluid dynamics%"
            OR LOWER(OriginalAffiliation) like "%sustainable engineering%"
            OR LOWER(OriginalAffiliation) like "%geopolymer%"
                THEN "School of Civil and Mechanical Engineering"
        WHEN
            LOWER(OriginalAffiliation) like "%chemical engineering%"
            OR LOWER(OriginalAffiliation) like "%school of mine%"
            OR LOWER(OriginalAffiliation) like "%mining%"
            OR LOWER(OriginalAffiliation) like "%petroleum%"
            OR LOWER(OriginalAffiliation) like "fuel% and energy technology institute%" --FETI
            OR LOWER(OriginalAffiliation) like "%advanced energy science%"
            OR LOWER(OriginalAffiliation) like "%chem. & pet. eng%"
            OR LOWER(OriginalAffiliation) like "%co2crc%"
                THEN "WASM Minerals, Energy and Chemical Engineering"
        WHEN
            LOWER(OriginalAffiliation) like "%electrical%engineering%"
            OR LOWER(OriginalAffiliation) like "%electr. & comput.%"
            OR LOWER(OriginalAffiliation) like "%math%"
            OR LOWER(OriginalAffiliation) like "%computer%"
            OR LOWER(OriginalAffiliation) like "%computing%"
            OR LOWER(OriginalAffiliation) like "%dept. of comput.%"
            OR LOWER(OriginalAffiliation) like "%radio astronomy%"
            OR LOWER(OriginalAffiliation) like "%icrar%"
            OR LOWER(OriginalAffiliation) like "%eecms%"
                THEN "School of Elec Eng, Comp and Math Sci"
        WHEN
            LOWER(OriginalAffiliation) like "%molecular%life science%"
            OR LOWER(OriginalAffiliation) like "%life%molecular science%"
            OR LOWER(OriginalAffiliation) like "%molecules%"
            OR LOWER(OriginalAffiliation) like "%molecular%"
            OR LOWER(OriginalAffiliation) like "%chemistry%"
            OR LOWER(OriginalAffiliation) like "%pharmacy%"
            OR LOWER(OriginalAffiliation) like "%sch. pharm.%"
            OR LOWER(OriginalAffiliation) like "%agriculture%"
            OR LOWER(OriginalAffiliation) like "%environment%"
            OR LOWER(OriginalAffiliation) like "%materials research%"
            OR LOWER(OriginalAffiliation) like "%water quality%"
                THEN "School of Molecular and Life Sciences"
        WHEN
            LOWER(OriginalAffiliation) like "%nursing%"
                THEN "School of Nursing"
        WHEN
            LOWER(OriginalAffiliation) like "%marketing%"
            OR LOWER(OriginalAffiliation) like "%management%"
            OR LOWER(OriginalAffiliation) like "%business%"
            OR LOWER(OriginalAffiliation) like "%economics%"
            OR LOWER(OriginalAffiliation) like "%accounting%"
            OR LOWER(OriginalAffiliation) like "%finance%"
            OR LOWER(OriginalAffiliation) like "%debi%"
            OR LOWER(OriginalAffiliation) like "%dig%ecosys%bus%intell%"
            OR LOWER(OriginalAffiliation) like "grad. sch. of bus."
                THEN "School of Management and Marketing"

        WHEN
            LOWER(OriginalAffiliation) like "%education%"
                THEN "School of Education"
        WHEN
            LOWER(OriginalAffiliation) like "%earth%"
            OR LOWER(OriginalAffiliation) like "%physics%"
            OR LOWER(OriginalAffiliation) like "%geology%"
            OR LOWER(OriginalAffiliation) like "%geography%"
            OR LOWER(OriginalAffiliation) like "%geoscience%" -- Geodesy and Inst for Geoscience Research
            OR LOWER(OriginalAffiliation) like "%gnss%"
            OR LOWER(OriginalAffiliation) like "%spatial%"
            OR LOWER(OriginalAffiliation) like "%antimatter%matter studies%"
            OR LOWER(OriginalAffiliation) like "%marine sci%" -- CMST
            OR LOWER(OriginalAffiliation) like "%space science%" -- CMST
            OR LOWER(OriginalAffiliation) like "%remote sensing%"
            THEN "School of Earth and Planetary Sciences"
        WHEN
            LOWER(OriginalAffiliation) like "%design%"
            OR LOWER(OriginalAffiliation) like "%built%"
            OR LOWER(OriginalAffiliation) like "%architecture%"
            OR LOWER(OriginalAffiliation) like "%infrastructur%"
            OR LOWER(OriginalAffiliation) like "%urban%regional planning%"
            OR LOWER(OriginalAffiliation) like "%planning and geography%"
            OR LOWER(OriginalAffiliation) like "%sustainability policy%" -- CUSP
            OR LOWER(OriginalAffiliation) like "%building information%"
                THEN "School of Design and the Built Environment"
        WHEN
            LOWER(OriginalAffiliation) like "%media%creative%"
            -- OR LOWER(OriginalAffiliation) like "%information systems%"
            OR LOWER(OriginalAffiliation) like "%culture%technology%" --CCAT
            OR LOWER(OriginalAffiliation) like "%internet studies%"
            OR LOWER(OriginalAffiliation) like "%social sciences%"
            OR LOWER(OriginalAffiliation) like "%information studies%"
            OR LOWER(OriginalAffiliation) like "%cultural studies%"
            OR LOWER(OriginalAffiliation) like "%theatre%screen%"
                THEN "School of Media, Creative Arts and Social Inquiry"
        WHEN
            LOWER(OriginalAffiliation) like "%information system%"
            OR LOWER(OriginalAffiliation) like "%inf. syst%"
                THEN "School of Information Systems"
        WHEN
            LOWER(OriginalAffiliation) like "%future of work%"
                THEN "FOWI"
        WHEN
            LOWER(OriginalAffiliation) like "%cancer prevention research%"
            OR LOWER(OriginalAffiliation) like "%behavioural research%cancer control%"
                THEN "WACRU"
        WHEN
            LOWER(OriginalAffiliation) like "%action on alcohol and youth%"
                THEN "MCAAY"
        WHEN
            LOWER(OriginalAffiliation) like "%national drug research institute%"
                THEN "NDRI"
        WHEN
            LOWER(OriginalAffiliation) like "%physical activity%"
            OR LOWER(OriginalAffiliation) like "%sport and recreation%"
                THEN "PAW"
        WHEN
            LOWER(OriginalAffiliation) like "%data linkage%"
                THEN "CDL"
        WHEN
            LOWER(OriginalAffiliation) like "%laeter%"
            OR LOWER(OriginalAffiliation) like "%argon isotope%"
                THEN "JDLC"
        WHEN
            LOWER(OriginalAffiliation) like "%curtin institute for computation%"
            OR LOWER(OriginalAffiliation) like "%curtin institute of computation%"
                THEN "CIC"
        WHEN
            LOWER(OriginalAffiliation) like "%health innovation research institute%"
                THEN "CHIRI"
        WHEN
            LOWER(OriginalAffiliation) like "%john curtin%public policy%"
                THEN "JCIPP"
        WHEN
            LOWER(OriginalAffiliation) like "%aboriginal studies%"
                THEN "CAS"
        WHEN
            LOWER(OriginalAffiliation) like "%malaysia%"
                THEN "Curtin Malaysia"
        WHEN
            LOWER(OriginalAffiliation) like "%faculty of health sciences%"
                THEN "Other Health Sciences"
        WHEN
            LOWER(OriginalAffiliation) like "%faculty of science and engineering%"
                THEN "Other Science and Engineering"
        WHEN
            LOWER(OriginalAffiliation) like "%faculty of humanities%"
                THEN "Other Humanities"
        ELSE null -- OriginalAffiliation
        END as school,
        SUM(num_affs) as num_affs
    FROM `coki-scratch-space.curtin.mag_curtin_affiliation_strings`
    GROUP BY school
    ORDER BY num_affs DESC
