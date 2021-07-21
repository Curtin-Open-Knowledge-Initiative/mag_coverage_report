SELECT
    doi,
    CASE
        WHEN
            affs.OriginalAffiliation = "Curtin University"
            OR affs.OriginalAffiliation = "Curtin University,Australia"
            OR affs.OriginalAffiliation = "Curtin University, Australia"
            OR affs.OriginalAffiliation = "Curtin Univ. of Technology (Australia)"
            OR affs.OriginalAffiliation = "Curtin University,Bentley,Western Australia,Australia."
            OR affs.OriginalAffiliation = "Curtin University  Perth WA"
            OR affs.OriginalAffiliation = "1Curtin University, Perth, Australia"
            OR affs.OriginalAffiliation = "Curtin Univ. of Technology, Perth, WA, Australia"
            OR affs.OriginalAffiliation = "Curtin University of Technology , Perth, Western Australia, Australia"
            OR affs.OriginalAffiliation = "Curtin University of Technology , Perth, Western Australia, Australia"
            OR affs.OriginalAffiliation = "Curtin University, Kent Street, Bentley, WA 6102, Australia#TAB#"
            OR affs.OriginalAffiliation = "Curtin University of Technology , Perth, Western Australia, Australia"
            OR affs.OriginalAffiliation = "Curtin Univ. of Technol. ., Perth"
            OR affs.OriginalAffiliation = "1 Curtin University, Perth, Western Australia, Australia."
            OR LOWER(affs.OriginalAffiliation) like "curtin university%perth"
            OR LOWER(affs.OriginalAffiliation) like "curtin university%perth%australia"
            OR LOWER(affs.OriginalAffiliation) like "curtin university%perth%australia,"
            OR LOWER(affs.OriginalAffiliation) like "curtin univ%bentley%australia"
            OR LOWER(affs.OriginalAffiliation) = "curtin university of technology"
            OR LOWER(affs.OriginalAffiliation) = "curtin#n#          university of technology"
            OR LOWER(affs.OriginalAffiliation) = "curtin university of technology perth, australia#tab#"
                THEN "Not Assigned"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%public health%"
            OR LOWER(affs.OriginalAffiliation) like "%public heath%"
            OR LOWER(affs.OriginalAffiliation) like "%population health%"
            OR LOWER(affs.OriginalAffiliation) like "%psychology%"
            OR LOWER(affs.OriginalAffiliation) like "%accident research centre%" -- C-MARC
                THEN "School of Population Health"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%allied health%"
            OR LOWER(affs.OriginalAffiliation) like "%physiotherapy%"
            OR LOWER(affs.OriginalAffiliation) like "%occupational therapy%"
                THEN "School of Allied Health"
        WHEN LOWER(affs.OriginalAffiliation)
            like "%medical%"
            THEN "Curtin Medical School"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%curtin law%"
                THEN "Curtin Law School"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%civil%mechanical%"
            OR LOWER(affs.OriginalAffiliation) like "%civil%engineering%"
            OR LOWER(affs.OriginalAffiliation) like "%civil%engneering%"
            OR LOWER(affs.OriginalAffiliation) like "%mech. eng.%"
            OR LOWER(affs.OriginalAffiliation) like "%mechanical%engineering%"
            OR LOWER(affs.OriginalAffiliation) like "%fluid dynamics%"
            OR LOWER(affs.OriginalAffiliation) like "%sustainable engineering%"
            OR LOWER(affs.OriginalAffiliation) like "%geopolymer%"
                THEN "School of Civil and Mechanical Engineering"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%chemical engineering%"
            OR LOWER(affs.OriginalAffiliation) like "%school of mine%"
            OR LOWER(affs.OriginalAffiliation) like "%mining%"
            OR LOWER(affs.OriginalAffiliation) like "%petroleum%"
            OR LOWER(affs.OriginalAffiliation) like "fuel% and energy technology institute%" --FETI
            OR LOWER(affs.OriginalAffiliation) like "%advanced energy science%"
            OR LOWER(affs.OriginalAffiliation) like "%chem. & pet. eng%"
            OR LOWER(affs.OriginalAffiliation) like "%co2crc%"
                THEN "WASM Minerals, Energy and Chemical Engineering"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%electrical%engineering%"
            OR LOWER(affs.OriginalAffiliation) like "%electr. & comput.%"
            OR LOWER(affs.OriginalAffiliation) like "%math%"
            OR LOWER(affs.OriginalAffiliation) like "%computer%"
            OR LOWER(affs.OriginalAffiliation) like "%computing%"
            OR LOWER(affs.OriginalAffiliation) like "%curtin institute for computation%"
            OR LOWER(affs.OriginalAffiliation) like "%curtin institute of computation%"
            OR LOWER(affs.OriginalAffiliation) like "%dept. of comput.%"
            OR LOWER(affs.OriginalAffiliation) like "%radio astronomy%"
            OR LOWER(affs.OriginalAffiliation) like "%icrar%"
            OR LOWER(affs.OriginalAffiliation) like "%eecms%"
                THEN "School of Elec Eng, Comp and Math Sci"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%molecular%life science%"
            OR LOWER(affs.OriginalAffiliation) like "%life%molecular science%"
            OR LOWER(affs.OriginalAffiliation) like "%molecules%"
            OR LOWER(affs.OriginalAffiliation) like "%molecular%"
            OR LOWER(affs.OriginalAffiliation) like "%chemistry%"
            OR LOWER(affs.OriginalAffiliation) like "%pharmacy%"
            OR LOWER(affs.OriginalAffiliation) like "%sch. pharm.%"
            OR LOWER(affs.OriginalAffiliation) like "%agriculture%"
            OR LOWER(affs.OriginalAffiliation) like "%environment%"
            OR LOWER(affs.OriginalAffiliation) like "%materials research%"
            OR LOWER(affs.OriginalAffiliation) like "%water quality%"
                THEN "School of Molecular and Life Sciences"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%nursing%"
                THEN "School of Nursing"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%marketing%"
            OR LOWER(affs.OriginalAffiliation) like "%management%"
            OR LOWER(affs.OriginalAffiliation) like "%business%"
            OR LOWER(affs.OriginalAffiliation) like "%debi%"
            OR LOWER(affs.OriginalAffiliation) like "%dig%ecosys%bus%intell%"
            OR LOWER(affs.OriginalAffiliation) like "grad. sch. of bus."
                THEN "School of Management & Marketing"
         WHEN
            LOWER(affs.OriginalAffiliation) like  "%economics%"
            OR LOWER(affs.OriginalAffiliation) like "%accounting%"
            OR LOWER(affs.OriginalAffiliation) like "%finance%"
                THEN "School of Accounting, Economics and Finance"

        WHEN
            LOWER(affs.OriginalAffiliation) like "%education%"
                THEN "School of Education"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%earth%"
            OR LOWER(affs.OriginalAffiliation) like "%physics%"
            OR LOWER(affs.OriginalAffiliation) like "%geology%"
            OR LOWER(affs.OriginalAffiliation) like "%geography%"
            OR LOWER(affs.OriginalAffiliation) like "%geoscience%" -- Geodesy and Inst for Geoscience Research
            OR LOWER(affs.OriginalAffiliation) like "%gnss%"
            OR LOWER(affs.OriginalAffiliation) like "%spatial%"
            OR LOWER(affs.OriginalAffiliation) like "%antimatter%matter studies%"
            OR LOWER(affs.OriginalAffiliation) like "%marine sci%" -- CMST
            OR LOWER(affs.OriginalAffiliation) like "%space science%" -- CMST
            OR LOWER(affs.OriginalAffiliation) like "%remote sensing%"
            THEN "School of Earth and Planetary Sciences"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%design%"
            OR LOWER(affs.OriginalAffiliation) like "%built%"
            OR LOWER(affs.OriginalAffiliation) like "%architecture%"
            OR LOWER(affs.OriginalAffiliation) like "%infrastructur%"
            OR LOWER(affs.OriginalAffiliation) like "%urban%regional planning%"
            OR LOWER(affs.OriginalAffiliation) like "%planning and geography%"
            OR LOWER(affs.OriginalAffiliation) like "%sustainability policy%" -- CUSP
            OR LOWER(affs.OriginalAffiliation) like "%building information%"
                THEN "School of Design and the Built Environment"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%media%creative%"
            -- OR LOWER(affs.OriginalAffiliation) like "%information systems%"
            OR LOWER(affs.OriginalAffiliation) like "%culture%technology%" --CCAT
            OR LOWER(affs.OriginalAffiliation) like "%internet studies%"
            OR LOWER(affs.OriginalAffiliation) like "%social sciences%"
            OR LOWER(affs.OriginalAffiliation) like "%information studies%"
            OR LOWER(affs.OriginalAffiliation) like "%cultural studies%"
            OR LOWER(affs.OriginalAffiliation) like "%theatre%screen%"
                THEN "School of Media, Creative Arts and Social Inquiry"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%information system%"
            OR LOWER(affs.OriginalAffiliation) like "%inf. syst%"
                THEN "School of Information Systems"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%future of work%"
                THEN "FOWI"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%cancer prevention research%"
            OR LOWER(affs.OriginalAffiliation) like "%behavioural research%cancer control%"
                THEN "WACRU"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%action on alcohol and youth%"
                THEN "MCAAY"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%national drug research institute%"
                THEN "NDRI"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%physical activity%"
            OR LOWER(affs.OriginalAffiliation) like "%sport and recreation%"
                THEN "PAW"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%data linkage%"
                THEN "CDL"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%laeter%"
            OR LOWER(affs.OriginalAffiliation) like "%argon isotope%"
                THEN "JDLC"

        WHEN
            LOWER(affs.OriginalAffiliation) like "%health innovation research institute%"
                THEN "CHIRI"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%john curtin%public policy%"
                THEN "JCIPP"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%aboriginal studies%"
                THEN "CAS"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%malaysia%"
                THEN "Curtin Malaysia"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%faculty of health sciences%"
                THEN "Other Health Sciences"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%faculty of science and engineering%"
                THEN "Other Science and Engineering"
        WHEN
            LOWER(affs.OriginalAffiliation) like "%faculty of humanities%"
                THEN "Other Humanities"
        ELSE "Not Assigned" -- affs.OriginalAffiliation
        END as school

FROM `academic-observatory.observatory_intermediate.mag20210626`, UNNEST(authors) as affs
WHERE affs.GridId = "grid.1032.0"
GROUP BY school, doi