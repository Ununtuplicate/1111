from __future__ import unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Collection, Page
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from .blocks import BaseStreamBlock

class StandardPage(Page):
    """
    Generic content page
    Can be used for any page type that only requires: title, image, introduction, body
    """
    
    introduction = models.TextField(
        help_text='Text to describe this page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000 and 3000px.'
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )
    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        StreamFieldPanel('body'),
        ImageChooserPanel('image'),
    ]
    
class NewHomePage(Page):
    """
    Home Page, split into:
    - Hero area (image with text caption or overlay)
    - Body area
    - Promotion area
    - Moveable featured site sections
    """
    
    # Hero area
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Homepage image'
    )
    hero_text = models.CharField(
        max_length=255,
        help_text='Write an introduction for your website'
    )
    hero_cta = models.CharField(
        verbose_name='Hero CTA',
        max_length=255,
        help_text='Text to display on Call to Action'
    )
    hero_cta_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Hero CTA link',
        help_text='Choose a page to link as your Call to Action'
    )
    
    # Body area
    body = StreamField(
        BaseStreamBlock(), verbose_name="Home content block", blank=True
    )
    
    # Promotional section of HomePage
    promo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Promotional Image'
    )
    promo_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above your promotional image'
    )
    promo_text = RichTextField(
        null=True,
        blank=True,
        help_text='Write the text for your promotional area here'
    )
    
    # Featured sections on HomePage
    # templates/base/home_page.html
    # treated differently, appear in different areas of HomePage
    # each list their children items that are accessed via children function
    # children function defined on individual Page models (BlogPage, BlogIndexPage, etc)
    featured_section_1_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above this featured section'
    )
    featured_section_1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='First featured section for HomePage. Displays up to three child items',
        verbose_name='Featured section 1'
    )
    
    featured_section_2_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above this featured section'
    )
    featured_section_2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Second featured section for HomePage. Displays up to three child items',
        verbose_name='Featured section 2'
    )
    
    featured_section_3_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above this featured section'
    )
    featured_section_3 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Third featured section for HomePage. Displays up to six child items',
        verbose_name='Featured section 3'
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('image'),
            FieldPanel('hero_text', classname="full"),
            MultiFieldPanel([
                FieldPanel('hero_cta'),
                PageChooserPanel('hero_cta_link'),
                ])
            ], heading="Hero section"),
        MultiFieldPanel([
            ImageChooserPanel('promo_image'),
            FieldPanel('promo_title'),
            FieldPanel('promo_text'),
        ], heading="Promo section"),
        StreamFieldPanel('body'),
        MultiFieldPanel([
            MultiFieldPanel([
                FieldPanel('featured_section_1_title'),
                PageChooserPanel('featured_section_1'),    
                ]),
            MultiFieldPanel([
                FieldPanel('featured_section_2_title'),
                PageChooserPanel('featured_section_2'),
                ]),
            MultiFieldPanel([
                FieldPanel('featured_section_3_title'),
                PageChooserPanel('featured_section_3'),
                ])
        ], heading="Featured homepage sections", classname="collapsible")
    ]
    
    def __str__(self):
        return self.title
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
