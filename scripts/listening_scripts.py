# -*- coding: utf-8 -*-
"""
Spoken IELTS Listening scripts. The MP3 files and the tapescripts are both built from this file.

Each section has an intro for the narrator, a voice per speaker, and a list of (speaker, text) turns.
In a turn, [shown|spoken] keeps the written form for the tapescript and the spelled-out form
for the voice, for example [650 pounds|six hundred and fifty pounds].
"""
import re

NARRATOR_VOICE = "bm_george"

SECTIONS = {
    (1, 1): {
        "intro": "Section one. You will hear a telephone conversation between a university housing officer and a new student.",
        "voices": {"Sarah": "bf_emma", "Alex": "bm_george"},
        "turns": [
            ("Sarah", "Good morning, University Housing Office, Sarah speaking. How can I help you?"),
            ("Alex", "Oh, hello. I'm starting a postgraduate course here in the autumn, and I was told to ring you about accommodation."),
            ("Sarah", "Of course. Congratulations on your place. Are you looking for a room in a hall of residence, or something more independent?"),
            ("Alex", "I'd really prefer a self-contained flat, if that's possible. I shared a house during my first degree and I found it hard to study, so this time I'd like my own space. Ideally it would be near the north campus, because that's where my department is."),
            ("Sarah", "That should be fine. We still have a few flats on our list, although they do go quickly at this time of year. Let me open a new enquiry for you. Can I take your name?"),
            ("Alex", "Yes, it's Alex Turner."),
            ("Sarah", "Is that Turner with a U?"),
            ("Alex", "That's right. [T-U-R-N-E-R|T, U, R, N, E, R]."),
            ("Sarah", "Thank you, Alex. And when would you need to move in? Most of our postgraduates arrive in the first week of September."),
            ("Alex", "Well, my course doesn't begin until the twenty-second, but I want a week to settle in. So I'd like to move in from September [15th|the fifteenth], if that works."),
            ("Sarah", "No problem at all. I'll put that down. And what's the best number to reach you on?"),
            ("Alex", "My mobile is the best. It's [07892 451209|oh seven eight nine two, four five one, two oh nine]."),
            ("Sarah", "Let me read that back. [07892 451209|oh seven eight nine two, four five one, two oh nine]."),
            ("Alex", "Yes, that's it."),
            ("Sarah", "Lovely. Now, I can see two flats that might suit you. The first one is on Station Road, but that's actually closer to the south campus, and it would take you about half an hour to walk to your department."),
            ("Alex", "Hmm, that's a bit far, isn't it?"),
            ("Sarah", "It is. The better choice is a one-bedroom flat at number 14, Meadowbank Road. That's Meadowbank, all one word."),
            ("Alex", "Meadowbank Road. And how far is that from the north campus?"),
            ("Sarah", "It's about ten minutes on foot, and there's a small supermarket on the corner too."),
            ("Alex", "That sounds perfect. How much is the rent?"),
            ("Sarah", "Last year it was six hundred and twenty pounds a month, but it's gone up slightly. It's now [650 pounds|six hundred and fifty pounds] a month."),
            ("Alex", "OK. And what does that cover?"),
            ("Sarah", "The rent includes your water rates, and it also includes high-speed broadband, which most students find very useful."),
            ("Alex", "Oh, good. So I wouldn't need to set up my own internet connection. What about the heating and lighting?"),
            ("Sarah", "The flat doesn't use gas, so everything runs on electricity, and electricity is billed separately. There's a smart meter in the kitchen, so you only pay for what you use."),
            ("Alex", "That seems fair. Is there a deposit to pay?"),
            ("Sarah", "Yes. Most private landlords ask for a full month's rent, but this flat is part of the university scheme, so the refundable security deposit is only [400 pounds|four hundred pounds]. You pay that when you sign, and you get it back when you leave, as long as the flat is in good condition."),
            ("Alex", "And how long is the contract for? My taught course only lasts nine months, you see."),
            ("Sarah", "I'm afraid the tenancy agreement runs for a minimum term of [12 months|twelve months]. Some students stay on over the summer to write their dissertation, and others find somebody to take over the flat."),
            ("Alex", "I can live with that. I'll be writing my dissertation over the summer anyway."),
            ("Sarah", "Great. To secure the reservation, you'll need to transfer the deposit this week. After that, please email us a copy of your passport, so that we can confirm your identity. You don't need to send your offer letter, because we can already see that on our system."),
            ("Alex", "Right, so the deposit, and then a copy of my passport. I'll do that this afternoon."),
            ("Sarah", "Perfect. You'll get a confirmation email from me within two working days."),
            ("Alex", "Thanks very much for your help, Sarah."),
            ("Sarah", "You're welcome, Alex. Goodbye."),
        ],
    },
    (1, 2): {
        "intro": "Section two. You will hear a coordinator speaking to new volunteers at a botanical garden.",
        "voices": {"Helen": "af_heart"},
        "turns": [
            ("Helen", "Good morning, everyone, and welcome to the Royal Botanical Gardens volunteer orientation. My name's Helen, and I look after our volunteer programme. Thank you all for giving up your Saturday morning. I'll spend about ten minutes telling you how the gardens work, and then we'll walk around together."),
            ("Helen", "Let me begin with a little history, because visitors will ask you about it. The gardens themselves are more than a hundred and fifty years old, but our newest and most popular building is the solar-powered tropical glasshouse. Work on it began in [2020|twenty twenty], and we hoped to finish it by the following summer, but there were long delays with the glass. It was officially opened in [2022|twenty twenty-two], and it now produces almost all of its own electricity. We're also hoping it will win a national design award in [2024|twenty twenty-four]."),
            ("Helen", "Before we go any further, here's a practical point. Please don't carry heavy backpacks along the paths with you. The Welcome Center only has room for our leaflets, and the Ticket Office is for staff who handle money. All personal belongings must be stored in the Staff Pavilion lockers. You'll be given a key at the end of this session."),
            ("Helen", "Now, one part of the glasshouse is closed at the moment, and that's our rare Amazonian orchid collection. Last spring we found insects damaging the plants. In the past we would have used chemical spraying, but that can harm the flowers themselves, and ultrasonic sound simply doesn't work on these insects. So the collection is currently undergoing biological pest control using predatory mites. These tiny creatures eat the pests and do no harm at all to the orchids. If visitors ask when it will reopen, just tell them it should be in a few weeks."),
            ("Helen", "Many of you will be helping with our guided walking tours. They used to leave once an hour, but they've become so popular that they now depart every [45 minutes|forty-five minutes]. Each tour lasts about an hour, and you don't need any special knowledge, because our gardeners lead them."),
            ("Helen", "During the summer we also need to think about the weather. In extreme heat, please direct visitors to the shaded mist pavilions, which are located along the southern pine walk. Don't send people down to the lake, because there's hardly any shade there."),
            ("Helen", "If somebody feels unwell, you should know where to go. Our emergency first aid stations are positioned next to the rose pavilion, right in the middle of the gardens. There's always a trained member of staff on duty there."),
            ("Helen", "I also have an invitation for you. The rose festival isn't until June, and the photo competition has moved to the autumn, but all volunteers are welcome at the heritage seed preservation seminar this Thursday afternoon. It's a great way to meet the staff."),
            ("Helen", "So what will your daily jobs be? At the start of each shift you'll collect a box of trail maps, and you'll distribute them to people as they arrive. You'll also show visitors where the guided tours begin, which is the fountain courtyard, just behind the main gate."),
            ("Helen", "And a final word about the people you'll meet. Local families usually know their way around, so they don't need much help. Most of the time you'll be assisting international visitors at the Welcome Center, so if you speak another language, please let me know."),
            ("Helen", "Right, that's everything for now. Let's collect your name badges, and then we'll start our walk."),
        ],
    },
    (1, 3): {
        "intro": "Section three. You will hear two engineering students, Mark and Chloe, discussing their project with their tutor.",
        "voices": {"Tutor": "bm_george", "Mark": "bm_fable", "Chloe": "bf_isabella"},
        "turns": [
            ("Tutor", "Come in, Mark. Come in, Chloe. Have a seat. I've read through your marine engineering proposal, and I think it's a promising start, but I do have some questions. First of all, why did you choose tidal stream turbines rather than offshore wind?"),
            ("Mark", "Well, we did look at wind first. Tidal turbines aren't cheaper to manufacture, and they're certainly not easier to reach for maintenance."),
            ("Chloe", "No, our main reason is the physics. Seawater is approximately [800 times|eight hundred times] denser than air, so even a slow current carries a lot of energy."),
            ("Tutor", "Good, that's justifiable. Now, what about the blades? I see you've chosen marine-grade stainless steel."),
            ("Mark", "Yes. We also looked at titanium alloy, but the cost was far too high."),
            ("Tutor", "I'd advise against steel. It's very heavy, and it will suffer in salt water. We recommend testing epoxy-coated carbon fiber composites instead."),
            ("Chloe", "Carbon fiber composites. They'd be lighter as well, wouldn't they?"),
            ("Tutor", "They would. Now, flow sensors. Where are you planning to mount them?"),
            ("Mark", "We thought we'd fix them to the turbine tower itself."),
            ("Tutor", "That would give you very noisy readings, because the blades disturb the water. They should go on seabed anchoring rigs, well away from the structure."),
            ("Chloe", "So, anchoring rigs on the seabed. OK, we'll change that in the diagram."),
            ("Tutor", "Next, your environmental risk matrix. You've written quite a lot about fish and seabirds, but you've missed the main issue."),
            ("Mark", "Do you mean the noise from the turbines?"),
            ("Tutor", "Exactly. Sound travels a long way under water, so your acoustic disruption tests must focus on marine mammals, such as seals and porpoises."),
            ("Chloe", "Marine mammals. Yes, we should have thought of that."),
            ("Tutor", "Now, deadlines. The final report isn't due until the end of term, and the presentation will be the week after that. But I need the revised CAD modeling parameters by Monday morning, because the workshop has to book time on the machines."),
            ("Mark", "Monday morning. That's fine, we can finish those this weekend."),
            ("Tutor", "Good. Let's go back to maintenance. What will be your biggest problem below the surface?"),
            ("Chloe", "Barnacles growing on the blades, along with rapid saltwater corrosion."),
            ("Tutor", "Right, but you've used the wrong term in your draft. You wrote cavitation, and in another place turbulence, and both of those mean something quite different. The word you need is biofouling. Marine biofouling is what barnacles cause."),
            ("Mark", "Sorry, we'll correct that."),
            ("Tutor", "No problem. And which sensors have you selected? Your first draft mentioned simple pressure gauges."),
            ("Chloe", "We've changed that. We're going to use acoustic Doppler sensors now."),
            ("Tutor", "Acoustic Doppler current profilers, yes. That's a much better choice. Those will measure the speed of the tidal current at several depths."),
            ("Mark", "And that data will feed straight into our energy model."),
            ("Tutor", "Excellent. In your conclusion, remind the reader of the main advantage of tidal energy. It isn't about warm water or low velocity. It's predictability. We can forecast the tides years in advance, which is something no wind farm can offer."),
            ("Chloe", "So, predictability. We'll make that the final point."),
            ("Tutor", "Good. Now I just need to complete the form for the department. This proposal is from Mark, and I always forget how you spell your name."),
            ("Chloe", "It's Chloe. [C-H-L-O-E|C, H, L, O, E]."),
            ("Tutor", "Thank you. Well done, both of you. I'll look forward to seeing those files on Monday."),
        ],
    },
    (1, 4): {
        "intro": "Section four. You will hear part of a university lecture about human working memory.",
        "voices": {"Lecturer": "bf_emma"},
        "turns": [
            ("Lecturer", "Good morning, everyone. In today's cognitive neuroscience lecture, we examine the architecture of human working memory. By working memory I mean the mental workspace that holds information for a short time while you use it, for example when you add up a restaurant bill in your head, or follow a set of directions."),
            ("Lecturer", "For many years, psychologists imagined short-term memory as a single store, a kind of box with limited space. That changed in the nineteen seventies, when Alan Baddeley and Graham Hitch proposed a system made up of separate parts. The first of these parts deals with sound, and it's called the phonological loop."),
            ("Lecturer", "The phonological loop stores speech-based information, such as a telephone number that somebody has just read out to you. The important point is how short-lived this store is. Unless you repeat the information to yourself, it stays in the loop for only about [2 seconds|two seconds]."),
            ("Lecturer", "The second part is the visuospatial sketchpad, which handles what we see and where things are. It keeps track of colour and spatial layout, and it also carries out mental rotations. If you've ever turned a sofa around in your imagination to decide whether it would fit through a door, you've been using your sketchpad."),
            ("Lecturer", "For more than twenty-five years, this was the accepted model. However, there were findings that it couldn't explain, such as how people recall whole stories. So Baddeley added a further component, the episodic buffer, in the year [2000|two thousand]."),
            ("Lecturer", "Let's turn now to the brain itself. Neuroimaging studies allow us to see which areas become active during these tasks. Spatial tasks draw more on the right side of the brain, while verbal working memory relies heavily on the left dorsolateral prefrontal cortex. That's a region just behind the forehead, and damage to it causes serious problems with planning."),
            ("Lecturer", "So what happens when the system is pushed too far? Think about trying to write a text message while crossing a busy road. Each task may be simple in itself, but cognitive overload occurs when the demands of the two tasks exceed the available attentional resources. At that point, performance on both tasks falls sharply."),
            ("Lecturer", "Let me finish by summarising the model, because this will be useful for your exam. At the top of the system sits the central executive, which supervises three slave systems: the loop, the sketchpad and the buffer."),
            ("Lecturer", "The central executive doesn't store anything itself. Its job is to coordinate attention between those systems, and to decide what deserves priority at any moment."),
            ("Lecturer", "Remember too that the memory trace in the phonological loop doesn't vanish all at once. Without rehearsal it's gradually lost through acoustic decay, and that is why we repeat numbers under our breath."),
            ("Lecturer", "And finally, multimodal binding, which means combining sounds, images and meaning into a single event, is carried out in the episodic buffer."),
            ("Lecturer", "That's all for today. Next week's seminar will be taken by Dr Vance, and Dr Miller will run the laboratory session on Friday. If you have any questions about this lecture, you can find me in my office on Tuesday afternoons. Just ask for Dr Hughes at the department reception. Thank you."),
        ],
    },
    (2, 1): {
        "intro": "Section one. You will hear a telephone conversation between a library assistant and a woman who wants to join the library.",
        "voices": {"Arthur": "bm_fable", "Elena": "bf_isabella"},
        "turns": [
            ("Arthur", "Good morning, Central City Library membership services, Arthur speaking."),
            ("Elena", "Hello. I've just moved to the city, and I'd like to join the library. Can I do that over the phone?"),
            ("Arthur", "You can certainly start your application over the phone. Would you like a temporary visitor's card or a full adult card?"),
            ("Elena", "A full adult library card, please. I'll be here for at least two years."),
            ("Arthur", "That's fine. Can I take your name?"),
            ("Elena", "Yes, my name's Elena Rostova."),
            ("Arthur", "Could you spell your surname for me?"),
            ("Elena", "Of course. It's [R-O-S-T-O-V-A|R, O, S, T, O, V, A]."),
            ("Arthur", "Thank you. And what's your address?"),
            ("Elena", "I recently moved to [28 Kensington Crescent|twenty-eight Kensington Crescent]. It's a large building, so you'll need the apartment number as well. That's apartment [4B|four B]."),
            ("Arthur", "Lovely, that's near the park, isn't it? And can I have a contact number?"),
            ("Elena", "We don't have a landline yet, so you'd better take my mobile number. It's [07731 998240|oh seven seven three one, nine nine eight, two four oh]."),
            ("Arthur", "Thanks. Now, let me tell you how membership works. Standard membership lets you borrow up to [8 books|eight books] at a time."),
            ("Elena", "Eight? That's better than my old library, which only allowed five."),
            ("Arthur", "That's right. You can also take out up to [4 audiobooks|four audiobooks], and those are counted separately from the books."),
            ("Elena", "That's great, I listen to them on the train. How long can I keep things?"),
            ("Arthur", "Films have to come back within seven days, but books and audiobooks can be kept for a period of [21 days|twenty-one days]."),
            ("Elena", "That's plenty. I'm also doing some research for my job, so I'd like to use the online databases. Is there a charge for those?"),
            ("Arthur", "Borrowing is free, but there's a one-off registration fee for access to the digital research databases. It was [20 pounds|twenty pounds] last year, but it's been reduced, so now you only pay [15 pounds|fifteen pounds]."),
            ("Elena", "That sounds reasonable. What do I need to bring with me when I collect my card?"),
            ("Arthur", "We need to see proof of your residential address. A passport won't do for that. The easiest thing is to bring a utility bill or a bank statement from the last three months."),
            ("Elena", "I've got a utility bill from last week, so I'll bring that. When are you open?"),
            ("Arthur", "Our central branch opens at [9:00 AM|nine AM] from Monday to Saturday. On Saturdays we close at five, but on weekdays we stay open until [8:00 PM|eight PM]."),
            ("Elena", "That's really helpful, because I work until six. Just one more question. What happens if I haven't finished a book by the end of the loan?"),
            ("Arthur", "You can extend the loan from your online account. Each item can be renewed online [2 times|two times] without a fine. After that, you'd need to bring it back, because somebody else may be waiting for it."),
            ("Elena", "That's great. Thank you very much for your help."),
            ("Arthur", "You're welcome. We look forward to seeing you. Goodbye."),
        ],
    },
    (2, 2): {
        "intro": "Section two. You will hear a guide giving information to visitors at a wildlife sanctuary.",
        "voices": {"Guide": "am_michael"},
        "turns": [
            ("Guide", "Good morning, visitors, and welcome to the Red Deer Valley Wildlife Sanctuary. My name's David, and I'm one of the rangers here. Before you set off, I'd like to tell you a little about the sanctuary and how to get the most out of your visit."),
            ("Guide", "When the sanctuary was founded in the nineteen eighties, it was just a small area around the old farm. Thanks to our supporters, it has grown steadily, and it now covers [450 hectares|four hundred and fifty hectares] of protected native woodland and wetland marsh. That makes it the largest reserve of its kind in the region."),
            ("Guide", "Most visitors come to see the birds. In winter, thousands of migratory waterfowl stop here on their way south. There are two small lakes in the valley, but the main observation hide is on Lake Heron, which you'll find on the eastern side of the marsh. To get there, you need to follow the oak trail. There's also a beech trail, but that one goes up the hill and away from the water, so don't take it by mistake."),
            ("Guide", "If you've brought children, I'd strongly recommend the feeding session at the otter enclosure. The afternoon session finished last year, so there's now just one each day, and it takes place at [10:30 AM|ten thirty AM]. Please arrive a few minutes early if you want to stand near the front."),
            ("Guide", "Now, I do need to mention our rules. You're welcome to bring cameras and water bottles anywhere in the sanctuary. However, bicycles and domestic pets are strictly prohibited inside the wetland conservation area. Dogs disturb the nesting birds, and bicycles damage the paths. There's a secure rack by the car park for bikes."),
            ("Guide", "If you'd like to look at the birds more closely, binoculars can be hired for the day. There's no rental charge, but we do ask for a [5 pound|five pound] deposit, which you'll get back when you return them."),
            ("Guide", "When you reach the wetland itself, it's really important to stay on the elevated timber boardwalks. You might be tempted to step off to take a photograph, but please don't. The ground here isn't what it looks like. It's made of fragile peat soil, which takes hundreds of years to form and can be damaged by a single footprint. The peat also stores a great deal of carbon, so protecting it matters far beyond this valley."),
            ("Guide", "Let me give you a couple of last tips. If you're heading for the lake, don't worry about the distance. Some of the signs say twenty-five minutes, but those are out of date. It's only about [15 minutes|fifteen minutes] on foot, even with young children."),
            ("Guide", "And if you can't tell a heron from a crane, don't worry. We've produced some excellent wildlife identification guides, and you can pick one up from the visitor desk, right behind me. Enjoy your day, and do tell us what you've seen when you come back."),
        ],
    },
    (2, 3): {
        "intro": "Section three. You will hear two students, Liam and Sophia, talking to their tutor about a research project on concrete.",
        "voices": {"Dr Patel": "bf_emma", "Liam": "bm_george", "Sophia": "af_bella"},
        "turns": [
            ("Liam", "Good afternoon, Dr Patel. It's Liam and Sophia, here to discuss our zero-carbon concrete project."),
            ("Dr Patel", "Come in, both of you. I've been looking forward to this. Remind me why you chose concrete as your topic."),
            ("Sophia", "Well, we were amazed by the size of the problem. Ordinary Portland cement contributes roughly [8 percent|eight percent] of total human carbon emissions."),
            ("Liam", "We'd seen a figure of four percent in an older article, and another one of fifteen percent online, but the [8 percent|eight percent] figure is the most reliable."),
            ("Dr Patel", "Good, make sure you cite your source for that. So how did you change the mixture?"),
            ("Sophia", "The main idea was to use less cement clinker, because that's what causes most of the emissions. We began by replacing thirty percent of it, and the results were so encouraging that we went further. In our final mixture we replaced [60 percent|sixty percent] of the clinker with industrial by-products."),
            ("Dr Patel", "That's a lot. Did the concrete keep its strength?"),
            ("Liam", "It did, and that was the surprising part. We carried out compressive strength testing in the laboratory at twenty-eight days, and the samples reached [48 megapascals|forty-eight megapascals]."),
            ("Dr Patel", "That's well above the structural benchmark. So what's the weakness?"),
            ("Sophia", "The curing rate. In normal conditions it's fine, but in sub-zero temperatures it's much slower than conventional concrete. That could cause problems on building sites in winter."),
            ("Dr Patel", "Yes, I expected that. Have you thought about how to solve it?"),
            ("Liam", "We considered heating the site, but that would use more energy and increase the carbon footprint. So we'd like to add a chemical activator. We've been reading about sodium silicate."),
            ("Dr Patel", "That's the right direction. Sodium silicate is widely used for this purpose. What's your next step?"),
            ("Sophia", "We want to carry out life-cycle carbon accounting, so that we're not only measuring emissions from production."),
            ("Dr Patel", "Good. Over what period?"),
            ("Liam", "We'd planned to look at twenty years, but we've been told that's too short."),
            ("Dr Patel", "It is. Buildings stand for much longer than that. Your model should use a simulated [50-year|fifty-year] structural lifespan."),
            ("Sophia", "OK, we'll change that."),
            ("Dr Patel", "Now, the department needs a cover sheet for this project, so let's make sure it's right. Your names go at the top. That's Liam, and Sophia. Don't let anybody call you Sarah or Emma again, as the last form did."),
            ("Sophia", "Thanks. I've had that problem all year!"),
            ("Dr Patel", "And I'm your supervisor, so put Dr Patel. That's [P-A-T-E-L|P, A, T, E, L]."),
            ("Liam", "Got it. What should we say in the summary?"),
            ("Dr Patel", "Keep it simple. State clearly which industrial by-product you used. You've written fly ash in one place, but your main ingredient was ground granulated blast-furnace slag, so mention that first."),
            ("Sophia", "Blast-furnace slag, yes. And we should explain the role of the activator, shouldn't we?"),
            ("Dr Patel", "Definitely. People often think that it speeds up drying, or that it stops cracking, but that isn't what it does. Explain that sodium silicate accelerates early hydration, which is the chemical reaction that gives concrete its strength."),
            ("Liam", "That's very clear. Thank you, Dr Patel."),
            ("Dr Patel", "You're welcome. It's excellent work so far, so keep it up."),
        ],
    },
    (2, 4): {
        "intro": "Section four. You will hear part of a university lecture about sleep.",
        "voices": {"Lecturer": "bm_george"},
        "turns": [
            ("Lecturer", "Good morning. Today's human physiology lecture examines circadian regulation and what we call sleep architecture. We spend around a third of our lives asleep, and yet until quite recently, sleep was treated as a passive state in which very little happened. We now know that the sleeping brain is remarkably busy."),
            ("Lecturer", "Let's begin with the structure of a normal night. Sleep isn't one continuous state. It's made up of cycles, in which the brain moves between non-rapid eye movement sleep, or NREM, and rapid eye movement sleep, or REM. These are called ultradian cycles, and each one lasts about [90 minutes|ninety minutes]. So a healthy adult will pass through four or five of them every night."),
            ("Lecturer", "The deepest part of the cycle is known as slow-wave sleep. During this stage, large groups of neurons fire together, and this produces synchronized delta brain waves. If we record these waves, we find that their frequency ranges from [0.5 to 4 Hertz|nought point five to four hertz]. It's very hard to wake someone at this point."),
            ("Lecturer", "So why does the brain need this deep sleep? One of the most exciting discoveries of recent years concerns waste removal. The rest of the body has a lymphatic system to carry away waste, but the brain doesn't. Instead, it depends on a separate network known as the glymphatic system. During deep sleep, the spaces between brain cells become wider, and fluid can flow through them more easily."),
            ("Lecturer", "This flow removes harmful substances from the tissue. The most important of these is a group of neurotoxic proteins called beta-amyloid. This matters because a build-up of these proteins is closely linked with Alzheimer's disease."),
            ("Lecturer", "Now let's consider how the timing of sleep is controlled. The key hormone here is melatonin, which is sometimes described as the signal of darkness. It's produced by the pineal gland, a tiny structure deep inside the brain."),
            ("Lecturer", "But the pineal gland doesn't decide when to produce it. That decision is made by the body's master clock, which is a small group of cells called the suprachiasmatic nucleus. This receives information about light directly from the eyes."),
            ("Lecturer", "That brings me to a modern problem. Phones and laptops give off a great deal of short-wavelength blue light. Research shows that the most powerful effect comes from wavelengths between 460 and [480 nanometers|four hundred and eighty nanometers]."),
            ("Lecturer", "The size of this effect is striking. Exposure to this light in the evening can suppress the production of melatonin by up to [85 percent|eighty-five percent], so the brain behaves as though it's still daytime."),
            ("Lecturer", "To return for a moment to the stages of sleep, you'll need to know the correct terms for your assignment. Stage N1 is the light sleep of drifting off, and N2 is a slightly deeper stage. Slow-wave deep sleep, which I described earlier, is officially known as Stage N3."),
            ("Lecturer", "And finally, why should any of this concern us? When our daily routine and our body clock don't match, for example in night-shift workers, we call this chronic circadian misalignment. The long-term studies are very clear about this. It significantly raises the risk of metabolic and cardiovascular disorders, including diabetes and heart disease. So a good night's sleep isn't a luxury. It's a biological necessity. Thank you."),
        ],
    },
}

_MARKUP = re.compile(r"\[([^\]|]+)\|([^\]]+)\]")


def shown(text):
    return _MARKUP.sub(r"\1", text)


def spoken(text):
    return _MARKUP.sub(r"\2", text)


def tapescript(test, section):
    """Readable transcript of a section. Monologues have no speaker labels."""
    data = SECTIONS[(test, section)]
    if len(data["voices"]) == 1:
        return "\n\n".join(shown(text) for _, text in data["turns"])
    return "\n".join(f"{speaker}: {shown(text)}" for speaker, text in data["turns"])
