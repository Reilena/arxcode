from django import forms
from evennia.objects.models import ObjectDB
from django.conf import settings
from django.db.models import Q
from world.msgs.models import Journal, Prayer


class JournalMarkAllReadForm(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset=Journal.objects.all(),
        widget=forms.MultipleHiddenInput,
        )


class JournalMarkOneReadForm(forms.Form):
    choice = forms.ModelChoiceField(
        queryset=Journal.objects.all(),
        widget=forms.HiddenInput,
        )


class JournalMarkFavorite(forms.Form):
    tagged = forms.ModelChoiceField(
        queryset=Journal.objects.all(),
        widget=forms.HiddenInput,
    )

    def tag_msg(self, char):
        msg = self.cleaned_data['tagged']
        msg.tag_favorite(char.player_ob)


class JournalRemoveFavorite(forms.Form):
    untagged = forms.ModelChoiceField(
        queryset=Journal.objects.all(),
        widget=forms.HiddenInput,
    )

    def untag_msg(self, char):
        msg = self.cleaned_data['untagged']
        msg.untag_favorite(char.player_ob)


class CharacterChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.key


class JournalWriteForm(forms.Form):

    journal = forms.CharField(
        label="Journal Text",
        widget=forms.Textarea(attrs={'class': "form-control",
                                     'rows': "10"}),
        )
    character = CharacterChoiceField(
        label="Character for Relationship Update",
        help_text="Leave blank if this journal is not a relationship",
        empty_label="(None - not a relationship)",
        required=False,
        queryset=ObjectDB.objects.filter(Q(db_typeclass_path=settings.BASE_CHARACTER_TYPECLASS) & Q(
            Q(roster__roster__name="Active") | Q(roster__roster__name="Gone") |
            Q(roster__roster__name="Available"))).order_by('db_key'),
    )
    private = forms.BooleanField(
        label="Black Journal",
        required=False,
        help_text="Mark if this is a private, black journal entry",
        )

    def create_journal(self, char):
        targ = self.cleaned_data['character']
        msg = self.cleaned_data['journal']
        white = not self.cleaned_data['private']
        if targ:
            # add a relationship
            char.messages.add_relationship(msg, targ, white)     
        else:
            # regular journal
            char.messages.add_journal(msg, white)

class PrayerMarkAllReadForm(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset=Prayer.objects.all(),
        widget=forms.MultipleHiddenInput,
        )


class PrayerMarkOneReadForm(forms.Form):
    choice = forms.ModelChoiceField(
        queryset=Prayer.objects.all(),
        widget=forms.HiddenInput,
        )


class PrayerMarkFavorite(forms.Form):
    tagged = forms.ModelChoiceField(
        queryset=Prayer.objects.all(),
        widget=forms.HiddenInput,
    )

    def tag_msg(self, char):
        msg = self.cleaned_data['tagged']
        msg.tag_favorite(char.player_ob)


class PrayerRemoveFavorite(forms.Form):
    untagged = forms.ModelChoiceField(
        queryset=Prayer.objects.all(),
        widget=forms.HiddenInput,
    )

    def untag_msg(self, char):
        msg = self.cleaned_data['untagged']
        msg.untag_favorite(char.player_ob)


class PrayerWriteForm(forms.Form):

    prayer = forms.CharField(
        label="Prayer Text",
        widget=forms.Textarea(attrs={'class': "form-control",
                                     'rows': "10"}),
        )
    character = CharacterChoiceField(
        label="God to pray to",
        help_text="A God must be chosen or the prayer will not work",
        empty_label="(List of Gods)",
        required=True,
        queryset=ObjectDB.objects.filter(Q(db_typeclass_path=settings.BASE_CHARACTER_TYPECLASS) & Q(
            Q(roster__roster__name="Gods"))).order_by('db_key'),
    )

    def create_prayer(self, char):
        targ = self.cleaned_data['character']
        msg = self.cleaned_data['prayer']
        char.messages.add_prayer(msg, targ)